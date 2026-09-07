from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

router = APIRouter()
DB_FILE = "db.json"

class ParticipantSchema(BaseModel):
    id: int
    trial_id: int
    participant_code: str
    status: str

@router.get("/", response_model=List[ParticipantSchema])
async def get_participants():
    if not os.path.exists(DB_FILE): return []
    with open(DB_FILE, "r") as f:
        return json.load(f).get("participants", [])

@router.post("/")
async def add_participant(p: ParticipantSchema):
    with open(DB_FILE, "r") as f:
        db = json.load(f)
    db["participants"].append(p.dict())
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)
    return p
