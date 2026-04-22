from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from app.database import get_db
from app.models import Kinase, Substrate
from app.schemas import SubstrateCreate, SubstrateResponse

router = APIRouter(prefix="/substrates", tags=["substrates"])

@router.post("/", response_model=SubstrateResponse, status_code=status.HTTP_201_CREATED)
async def create_substrate(
    substrate: SubstrateCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Add new substrate annotation with validation.
    
    Business Logic:
    - STK33 (pseudokinase) will reject substrates with 403 Forbidden
    - Duplicate substrates (same kinase + gene + site) return 409 Conflict
    """
    
    # Check if kinase exists
    kinase_result = await db.execute(
        select(Kinase).where(Kinase.kinase_id == substrate.kinase_id)
    )
    kinase = kinase_result.scalar_one_or_none()
    
    if not kinase:
        raise HTTPException(
            status_code=404,
            detail="Kinase not found"
        )
    
    # STK33 BUSINESS LOGIC: Reject substrates for confirmed pseudokinases
    if kinase.is_pseudokinase == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Catalytically inactive pseudokinase cannot have functional substrates."
        )
    
    # Check for duplicate (kinase + gene + site)
    duplicate_query = select(Substrate).where(
        Substrate.kinase_id == substrate.kinase_id,
        Substrate.substrate_gene == substrate.substrate_gene,
        Substrate.phospho_site == substrate.phospho_site
    )
    duplicate_result = await db.execute(duplicate_query)
    if duplicate_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Substrate already exists for this kinase"
        )
    
    # Create new substrate
    new_substrate = Substrate(
        substrate_id=f"SUB_{uuid.uuid4().hex[:12]}",
        kinase_id=substrate.kinase_id,
        substrate_gene=substrate.substrate_gene,
        phospho_site=substrate.phospho_site,
        evidence_source=substrate.evidence_source,
        curator_confidence=substrate.curator_confidence
    )
    
    db.add(new_substrate)
    await db.commit()
    await db.refresh(new_substrate)
    
    return new_substrate