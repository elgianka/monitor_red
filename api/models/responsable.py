from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..db.session import Base

class ResponsableBase(BaseModel):
    NOM_RESPONSABLE: str

class ResponsableCreate(ResponsableBase):
    pass

class Responsable(ResponsableBase):
    ID_RESPONSABLE: int

    class Config:
        from_attributes = True

class ResponsableDB(Base):
    __tablename__ = "TB_RESPONSABLE"

    ID_RESPONSABLE = Column(Integer, primary_key=True, index=True)
    NOM_RESPONSABLE = Column(String, nullable=False, unique=True)

    hosts = relationship("HostDB", back_populates="responsable")
