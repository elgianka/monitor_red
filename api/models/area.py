from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class AreaBase(BaseModel):
    NOM_AREA: str
    ID_GERENCIA: int

class AreaCreate(AreaBase):
    pass

class Area(AreaBase):
    ID_AREA: int

    class Config:
        from_attributes = True

class AreaDB(Base):
    __tablename__ = "TB_AREA"

    ID_AREA = Column(Integer, primary_key=True, index=True)
    NOM_AREA = Column(String, nullable=False, unique=True)
    ID_GERENCIA = Column(Integer, ForeignKey("TB_GERENCIA.ID_GERENCIA"))

    gerencia = relationship("GerenciaDB", back_populates="areas")
    responsables = relationship("ResponsableDB", back_populates="area")
