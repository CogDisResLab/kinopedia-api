from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Structure, AlphaFoldModel
from app.schemas import StructureResponse, AlphaFoldResponse

router = APIRouter(prefix="/structures", tags=["structures"])

@router.get("/pdb/{pdb_id}", response_model=StructureResponse)
async def get_pdb_structure(
    pdb_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get experimental structure metadata by PDB ID"""
    result = await db.execute(
        select(Structure).where(Structure.pdb_id == pdb_id.upper())
    )
    structure = result.scalar_one_or_none()
    
    if not structure:
        raise HTTPException(status_code=404, detail="PDB structure not found")
    
    return structure

@router.get("/alphafold/{protein_id}", response_model=AlphaFoldResponse)
async def get_alphafold_model(
    protein_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get AlphaFold model for a specific protein"""
    result = await db.execute(
        select(AlphaFoldModel).where(AlphaFoldModel.protein_id == protein_id)
    )
    model = result.scalar_one_or_none()
    
    if not model:
        raise HTTPException(status_code=404, detail="AlphaFold model not found")
    
    return model