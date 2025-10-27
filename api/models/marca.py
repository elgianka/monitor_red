from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from ..db.session import Base

class MarcaBase(BaseModel):
    NOM_MARCA: str

class MarcaCreate(MarcaBase):
    pass

class Marca(MarcaBase):
    ID_MARCA: int

    class Config:
        orm_mode = True

class MarcaDB(Base):
    __tablename__ = "TB_MARCA"

    ID_MARCA = Column(Integer, primary_key=True, index=True)
    NOM_MARCA = Column(String, nullable=False)
