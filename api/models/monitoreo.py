from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional
import datetime

from ..db.session import Base

# SQLAlchemy Model
class MonitoreoDB(Base):
    __tablename__ = "TB_MONITOREO"

    ID_MONITOREO = Column(Integer, primary_key=True, index=True)
    ID_HOST = Column(Integer, ForeignKey("TB_HOST.ID_HOST"))
    PING_RESULT = Column(Float)
    TIMESTAMP = Column(DateTime, default=datetime.datetime.now)

    host = relationship("HostDB", back_populates="monitoreos")

# Pydantic Model for API responses
class Monitoreo(BaseModel):
    ID_MONITOREO: int
    ID_HOST: int
    PING_RESULT: Optional[float] = None
    TIMESTAMP: datetime.datetime

    class Config:
        from_attributes = True

class MonitoreoCreate(BaseModel):
    ID_HOST: int
    PING_RESULT: Optional[float] = None
    TIMESTAMP: Optional[datetime.datetime] = None