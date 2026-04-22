from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Text, ForeignKey
from typing import Optional, List
from app.database import Base

class Kinase(Base):
    __tablename__ = "kinases"
    
    # Core required fields (these MUST exist)
    kinase_id: Mapped[str] = mapped_column(String, primary_key=True)
    hgnc_symbol: Mapped[str] = mapped_column(String, nullable=False)
    hgnc_id: Mapped[str] = mapped_column(String, nullable=False)
    hgnc_name: Mapped[str] = mapped_column(String, nullable=False)
    classification_group: Mapped[str] = mapped_column(String, nullable=False)
    
    # Optional fields (might or might not exist)
    classification_family: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_pseudokinase: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    pseudokinase_evidence: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    curator_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    proteins: Mapped[List["Protein"]] = relationship(back_populates="kinase", lazy="selectin")
    substrates: Mapped[List["Substrate"]] = relationship(back_populates="kinase", lazy="selectin")

class Protein(Base):
    __tablename__ = "proteins"
    
    protein_id: Mapped[str] = mapped_column(String, primary_key=True)
    kinase_id: Mapped[str] = mapped_column(ForeignKey("kinases.kinase_id"))
    uniprot_accession: Mapped[str] = mapped_column(String, nullable=False)
    protein_name: Mapped[str] = mapped_column(String, nullable=False)
    sequence_length: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    kinase_domain_start: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    kinase_domain_end: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Relationships
    kinase: Mapped["Kinase"] = relationship(back_populates="proteins", lazy="selectin")

class Substrate(Base):
    __tablename__ = "substrates"
    
    substrate_id: Mapped[str] = mapped_column(String, primary_key=True)
    kinase_id: Mapped[str] = mapped_column(ForeignKey("kinases.kinase_id"))
    substrate_gene: Mapped[str] = mapped_column(String, nullable=False)
    phospho_site: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    evidence_source: Mapped[str] = mapped_column(String, nullable=False)
    curator_confidence: Mapped[str] = mapped_column(String, nullable=False)
    
    # Relationships
    kinase: Mapped["Kinase"] = relationship(back_populates="substrates", lazy="selectin")

class Structure(Base):
    __tablename__ = "structures"
    
    structure_id: Mapped[str] = mapped_column(String, primary_key=True)
    protein_id: Mapped[str] = mapped_column(ForeignKey("proteins.protein_id"))
    pdb_id: Mapped[str] = mapped_column(String, nullable=False)
    resolution_angstrom: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ligand_bound: Mapped[Optional[str]] = mapped_column(String, nullable=True)

class AlphaFoldModel(Base):
    __tablename__ = "alphafold_models"
    
    model_id: Mapped[str] = mapped_column(String, primary_key=True)
    protein_id: Mapped[str] = mapped_column(ForeignKey("proteins.protein_id"))
    alphafold_id: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)

class ExternalID(Base):
    __tablename__ = "external_ids"
    
    xref_id: Mapped[str] = mapped_column(String, primary_key=True)
    kinase_id: Mapped[str] = mapped_column(ForeignKey("kinases.kinase_id"))
    database: Mapped[str] = mapped_column(String, nullable=False)
    identifier: Mapped[str] = mapped_column(String, nullable=False)

class DataConflict(Base):
    __tablename__ = "data_conflicts"
    
    conflict_id: Mapped[str] = mapped_column(String, primary_key=True)
    kinase_id: Mapped[str] = mapped_column(ForeignKey("kinases.kinase_id"))
    field_name: Mapped[str] = mapped_column(String, nullable=False)
    source_1: Mapped[str] = mapped_column(String, nullable=False)
    value_1: Mapped[str] = mapped_column(String, nullable=False)
    source_2: Mapped[str] = mapped_column(String, nullable=False)
    value_2: Mapped[str] = mapped_column(String, nullable=False)
    resolution: Mapped[str] = mapped_column(String, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)