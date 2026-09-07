from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.db_models import Participant as ParticipantModel, Trial as TrialModel
from app.models.schemas import ParticipantCreate, ParticipantOut

router = APIRouter()

@router.get("/", response_model=List[ParticipantOut])
def list_participants(db: Session = Depends(get_db)):
    return db.query(ParticipantModel).all()

@router.post("/", response_model=ParticipantOut)
def add_participant(participant: ParticipantCreate, db: Session = Depends(get_db)):
    trial = db.query(TrialModel).filter(TrialModel.id == participant.trial_id).first()
    if not trial:
        raise HTTPException(status_code=400, detail="trial_id does not match any existing trial")
    record = ParticipantModel(**participant.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.delete("/{participant_id}")
def delete_participant(participant_id: int, db: Session = Depends(get_db)):
    record = db.query(ParticipantModel).filter(ParticipantModel.id == participant_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Participant not found")
    db.delete(record)
    db.commit()
    return {"status": "deleted", "id": participant_id}
