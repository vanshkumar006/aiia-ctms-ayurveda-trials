from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.db_models import Trial as TrialModel
from app.models.schemas import TrialCreate, TrialOut

router = APIRouter()

@router.get("/", response_model=List[TrialOut])
def list_trials(db: Session = Depends(get_db)):
    return db.query(TrialModel).all()

@router.get("/{trial_id}", response_model=TrialOut)
def get_trial(trial_id: int, db: Session = Depends(get_db)):
    trial = db.query(TrialModel).filter(TrialModel.id == trial_id).first()
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    return trial

@router.post("/", response_model=TrialOut)
def create_trial(trial: TrialCreate, db: Session = Depends(get_db)):
    record = TrialModel(**trial.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.put("/{trial_id}", response_model=TrialOut)
def update_trial(trial_id: int, trial: TrialCreate, db: Session = Depends(get_db)):
    record = db.query(TrialModel).filter(TrialModel.id == trial_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Trial not found")
    for key, value in trial.model_dump().items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record

@router.delete("/{trial_id}")
def delete_trial(trial_id: int, db: Session = Depends(get_db)):
    record = db.query(TrialModel).filter(TrialModel.id == trial_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Trial not found")
    db.delete(record)
    db.commit()
    return {"status": "deleted", "id": trial_id}
