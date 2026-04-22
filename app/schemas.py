from pydantic import BaseModel, Field
from typing import Optional, List

# Kinase schemas
class KinaseBase(BaseModel):
    hgnc_symbol: str
    hgnc_name: str
    classification_group: str
    classification_family: Optional[str] = None

class KinaseResponse(KinaseBase):
    kinase_id: str
    hgnc_id: str
    is_pseudokinase: Optional[int] = None
    pseudokinase_evidence: Optional[str] = None
    
    class Config:
        from_attributes = True

class KinaseDetail(KinaseResponse):
    substrate_count: Optional[int] = 0
    structure_count: Optional[int] = 0

# Substrate schemas
class SubstrateBase(BaseModel):
    substrate_gene: str
    phospho_site: Optional[str] = None
    evidence_source: str
    curator_confidence: str

class SubstrateResponse(SubstrateBase):
    substrate_id: str
    kinase_id: str
    
    class Config:
        from_attributes = True

class SubstrateCreate(SubstrateBase):
    kinase_id: str

# Structure schemas
class StructureResponse(BaseModel):
    structure_id: str
    pdb_id: str
    resolution_angstrom: Optional[float] = None
    ligand_bound: Optional[str] = None
    
    class Config:
        from_attributes = True

class AlphaFoldResponse(BaseModel):
    model_id: str
    alphafold_id: str
    version: str
    url: str
    
    class Config:
        from_attributes = True

# Conflict schemas
class ConflictResponse(BaseModel):
    conflict_id: str
    kinase_id: str
    field_name: str
    source_1: str
    value_1: str
    source_2: str
    value_2: str
    resolution: str
    rationale: str
    
    class Config:
        from_attributes = True