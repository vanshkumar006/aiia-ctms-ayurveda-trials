from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.db_models import SafetyEvent as SafetyEventModel, Participant as ParticipantModel
from app.models.schemas import AdverseEventCreate, AdverseEventOut

router = APIRouter()

@router.get("/", response_model=List[AdverseEventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(SafetyEventModel).all()

@router.post("/", response_model=AdverseEventOut)
def report_event(event: AdverseEventCreate, db: Session = Depends(get_db)):
    participant = db.query(ParticipantModel).filter(ParticipantModel.id == event.participant_id).first()
    if not participant:
        raise HTTPException(status_code=400, detail="participant_id does not match any existing participant")
    record = SafetyEventModel(**event.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    record = db.query(SafetyEventModel).filter(SafetyEventModel.id == event_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(record)
    db.commit()
    return {"status": "deleted", "id": event_id}
