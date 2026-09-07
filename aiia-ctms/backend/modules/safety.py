from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

router = APIRouter()
DB_FILE = "db.json"

class AdverseEventSchema(BaseModel):
    id: int
    participant_id: int
    description: str
    severity: str # Mild, Moderate, Severe
    causality: str # Related, Unrelated

@router.get("/", response_model=List[AdverseEventSchema])
async def get_events():
    if not os.path.exists(DB_FILE): return []
    with open(DB_FILE, "r") as f:
        return json.load(f).get("safety_events", [])

@router.post("/")
async def report_event(e: AdverseEventSchema):
    with open(DB_FILE, "r") as f:
        db = json.load(f)
    db["safety_events"].append(e.dict())
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)
    return e
