from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class ModeloBase(BaseModel):
    NOM_MODELO: str
    ID_MARCA: int

class ModeloCreate(ModeloBase):
    pass

class Modelo(ModeloBase):
    ID_MODELO: int

    class Config:
        from_attributes = True

class ModeloDB(Base):
    __tablename__ = "TB_MODELO"

    ID_MODELO = Column(Integer, primary_key=True, index=True)
    NOM_MODELO = Column(String, nullable=False)
    ID_MARCA = Column(Integer, ForeignKey("TB_MARCA.ID_MARCA"))

    hosts = relationship("HostDB", back_populates="modelo")
    marca = relationship("MarcaDB", back_populates="modelos")
