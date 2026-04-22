from app.schemas import KinaseResponse, KinaseDetail, ConflictResponse, SubstrateResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.database import get_db
from app.models import Kinase, Substrate, DataConflict
from app.schemas import KinaseResponse, KinaseDetail, ConflictResponse

router = APIRouter(prefix="/kinases", tags=["kinases"])

@router.get("/", response_model=List[KinaseResponse])
async def list_kinases(
    group: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """List all kinases with optional filtering by classification group"""
    query = select(Kinase)
    
    if group:
        query = query.where(Kinase.classification_group == group)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    kinases = result.scalars().all()
    return kinases

@router.get("/{kinase_id}", response_model=KinaseDetail)
async def get_kinase(
    kinase_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific kinase"""
    # Get kinase
    result = await db.execute(select(Kinase).where(Kinase.kinase_id == kinase_id))
    kinase = result.scalar_one_or_none()
    
    if not kinase:
        raise HTTPException(status_code=404, detail="Kinase not found")
    
    # Count substrates
    substrate_count_query = select(func.count()).select_from(Substrate).where(
        Substrate.kinase_id == kinase_id
    )
    substrate_count = await db.scalar(substrate_count_query)
    
    # Create response
    kinase_dict = {
        "kinase_id": kinase.kinase_id,
        "hgnc_symbol": kinase.hgnc_symbol,
        "hgnc_id": kinase.hgnc_id,
        "hgnc_name": kinase.hgnc_name,
        "classification_group": kinase.classification_group,
        "classification_family": kinase.classification_family,
        "is_pseudokinase": kinase.is_pseudokinase,
        "pseudokinase_evidence": kinase.pseudokinase_evidence,
        "substrate_count": substrate_count or 0,
        "structure_count": 0
    }
    
    # Special handling for CASK (disputed activity)
    if kinase.hgnc_symbol == "CASK" and kinase.is_pseudokinase is None:
        kinase_dict["status"] = "disputed_activity"
        kinase_dict["note"] = "Literature contains conflicting reports on catalytic activity."
    
    return kinase_dict

@router.get("/{kinase_id}/substrates", response_model=List[SubstrateResponse])
async def get_kinase_substrates(
    kinase_id: str,
    confidence: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all substrates for a specific kinase"""
    # Check if kinase exists
    kinase_result = await db.execute(select(Kinase).where(Kinase.kinase_id == kinase_id))
    kinase = kinase_result.scalar_one_or_none()
    
    if not kinase:
        raise HTTPException(status_code=404, detail="Kinase not found")
    
    # Build query
    query = select(Substrate).where(Substrate.kinase_id == kinase_id)
    
    if confidence:
        query = query.where(Substrate.curator_confidence == confidence)
    
    result = await db.execute(query)
    substrates = result.scalars().all()
    return substrates

@router.get("/{kinase_id}/conflicts", response_model=List[ConflictResponse])
async def get_kinase_conflicts(
    kinase_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get documented conflicts for a specific kinase"""
    result = await db.execute(
        select(DataConflict).where(DataConflict.kinase_id == kinase_id)
    )
    conflicts = result.scalars().all()
    return conflicts