from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models import responsable as responsable_model, user as user_model
from ..db.session import get_db
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/responsables", response_model=responsable_model.Responsable, tags=["Responsables"])
def create_responsable(responsable: responsable_model.ResponsableCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_responsable = responsable_model.ResponsableDB(**responsable.dict())
    db.add(db_responsable)
    db.commit()
    db.refresh(db_responsable)
    return db_responsable

@router.get("/responsables", response_model=List[responsable_model.Responsable], tags=["Responsables"])
def get_responsables(db: Session = Depends(get_db)):
    responsables = db.query(responsable_model.ResponsableDB).all()
    return responsables

@router.get("/responsables/{id_responsable}", response_model=responsable_model.Responsable, tags=["Responsables"])
def get_responsable(id_responsable: int, db: Session = Depends(get_db)):
    responsable = db.query(responsable_model.ResponsableDB).filter(responsable_model.ResponsableDB.ID_RESPONSABLE == id_responsable).first()
    if responsable is None:
        raise HTTPException(status_code=404, detail="Responsable not found")
    return responsable

@router.put("/responsables/{id_responsable}", response_model=responsable_model.Responsable, tags=["Responsables"])
def update_responsable(id_responsable: int, responsable: responsable_model.ResponsableCreate, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_responsable = db.query(responsable_model.ResponsableDB).filter(responsable_model.ResponsableDB.ID_RESPONSABLE == id_responsable).first()
    if db_responsable is None:
        raise HTTPException(status_code=404, detail="Responsable not found")
    update_data = responsable.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_responsable, key, value)
    db.add(db_responsable)
    db.commit()
    db.refresh(db_responsable)
    return db_responsable

@router.delete("/responsables/{id_responsable}", status_code=204, tags=["Responsables"])
def delete_responsable(id_responsable: int, db: Session = Depends(get_db), current_user: user_model.UserDB = Depends(get_current_user)):
    db_responsable = db.query(responsable_model.ResponsableDB).filter(responsable_model.ResponsableDB.ID_RESPONSABLE == id_responsable).first()
    if db_responsable is None:
        raise HTTPException(status_code=404, detail="Responsable not found")
    db.delete(db_responsable)
    db.commit()
    return
