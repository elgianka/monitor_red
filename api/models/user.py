from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from ..db.session import Base

class UserBase(BaseModel):
    nom_usuario: str
    rol: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id_usuario: int

    class Config:
        orm_mode = True

class UserDB(Base):
    __tablename__ = "TB_USUARIOS_DEL_SISTEMA"

    id_usuario = Column("ID_USUARIO", Integer, primary_key=True, index=True)
    nom_usuario = Column("NOM_USUARIO", String, unique=True, index=True)
    password_hash = Column("PASSWORD_HASH", String)
    rol = Column("ROL", String)
