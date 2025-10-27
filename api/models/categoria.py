from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from ..db.session import Base

class CategoriaBase(BaseModel):
    NOM_CATEGORIA: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    ID_CATEGORIA: int

    class Config:
        orm_mode = True

class CategoriaDB(Base):
    __tablename__ = "TB_CATEGORIA"

    ID_CATEGORIA = Column(Integer, primary_key=True, index=True)
    NOM_CATEGORIA = Column(String, nullable=False)
