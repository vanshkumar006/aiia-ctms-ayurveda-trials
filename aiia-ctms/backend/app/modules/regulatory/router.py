from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.db_models import RegulatoryLog as RegulatoryLogModel
from app.models.schemas import RegulatoryLogCreate, RegulatoryLogOut

router = APIRouter()

@router.get("/", response_model=List[RegulatoryLogOut])
def list_logs(db: Session = Depends(get_db)):
    return db.query(RegulatoryLogModel).all()

@router.post("/", response_model=RegulatoryLogOut)
def add_log(log: RegulatoryLogCreate, db: Session = Depends(get_db)):
    record = RegulatoryLogModel(**log.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
