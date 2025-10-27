from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from ..db.session import Base

class EstadoBase(BaseModel):
    NOM_ESTADO: str

class EstadoCreate(EstadoBase):
    pass

class Estado(EstadoBase):
    ID_ESTADO: int

    class Config:
        orm_mode = True

class EstadoDB(Base):
    __tablename__ = "TB_ESTADO"

    ID_ESTADO = Column(Integer, primary_key=True, index=True)
    NOM_ESTADO = Column(String, nullable=False, unique=True)
