from typing import Optional
from pydantic import BaseModel, Field

class TrialCreate(BaseModel):
    title: str
    status: str = "Ethics Review"
    enrollment: int = 0
    ctri_id: Optional[str] = "Pending"
    target_sample_size: Optional[int] = 100
    protocol_number: Optional[str] = None
    phase: Optional[str] = None
    sponsor: Optional[str] = None

class TrialOut(TrialCreate):
    id: int

class ParticipantCreate(BaseModel):
    trial_id: int
    participant_code: str
    status: str = "Enrolled"
    consent: bool = True

class ParticipantOut(ParticipantCreate):
    id: int

class AdverseEventCreate(BaseModel):
    participant_id: int
    description: str
    severity: str = Field(description="Mild | Moderate | Severe | Serious (SAE)")
    causality: str = Field(description="Related | Possibly Related | Unrelated")

class AdverseEventOut(AdverseEventCreate):
    id: int

class RegulatoryLogCreate(BaseModel):
    trial_id: int
    event: str
    date: str

class RegulatoryLogOut(RegulatoryLogCreate):
    id: int

class TextAnalysisRequest(BaseModel):
    text: str
    model_preference: Optional[str] = "auto"  # "auto" | "cloud" | "local"

class PatientMatchRequest(BaseModel):
    patient_data: str
    trial_criteria: str
    model_preference: Optional[str] = "auto"

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    username: str
    role: str
    full_name: str

