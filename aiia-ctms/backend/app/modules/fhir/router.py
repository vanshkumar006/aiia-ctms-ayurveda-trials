from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.db_models import Trial as TrialModel

router = APIRouter()

@router.get("/export")
def export_fhir(db: Session = Depends(get_db)):
    trials = db.query(TrialModel).all()
    bundle = []
    status_map = {"Active": "active", "Ethics Review": "in-review", "Completed": "completed"}
    for trial in trials:
        bundle.append({
            "resourceType": "ResearchStudy",
            "id": str(trial.id),
            "status": status_map.get(trial.status, "unknown"),
            "title": trial.title,
            "identifier": [{"system": "CTRI", "value": trial.ctri_id or "Pending"}],
            "protocol": {"text": trial.protocol_number or "Ayurvedic Protocol v1.0"},
        })
    return {"resourceType": "Bundle", "type": "collection", "entry": bundle}
