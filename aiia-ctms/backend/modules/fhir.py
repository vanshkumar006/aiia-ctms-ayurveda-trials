from fastapi import APIRouter
import json

router = APIRouter()
DB_FILE = "db.json"

@router.get("/export")
async def export_fhir():
    with open(DB_FILE, "r") as f:
        db = json.load(f)
    
    # Simplified FHIR ResearchStudy mapping
    fhir_output = []
    for trial in db["trials"]:
        fhir_output.append({
            "resourceType": "ResearchStudy",
            "id": str(trial["id"]),
            "status": "active",
            "title": trial["title"],
            "protocol": {"text": "Ayurvedic Protocol v1.0"}
        })
    return {"fhir_bundle": fhir_output}
