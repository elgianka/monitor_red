from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from ..db.session import Base

class SedeBase(BaseModel):
    NOM_SEDE: str

class SedeCreate(SedeBase):
    pass

class Sede(SedeBase):
    ID_SEDE: int

    class Config:
        from_attributes = True

from sqlalchemy.orm import relationship

class SedeDB(Base):
    __tablename__ = "TB_SEDE"

    ID_SEDE = Column(Integer, primary_key=True, index=True)
    NOM_SEDE = Column(String, nullable=False)

    hosts = relationship("HostDB", back_populates="sede")
    ubicaciones = relationship("UbicacionDB", back_populates="sede_rel")
