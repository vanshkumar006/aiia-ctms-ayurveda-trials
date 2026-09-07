import datetime
import json
import requests
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.db_models import AIAnalysis as AIAnalysisModel
from app.models.schemas import PatientMatchRequest, TextAnalysisRequest
from ai_engine.processing.extractors import extract_text
from ai_engine.prompts.clinical_prompts import (
    DOCUMENT_ANALYSIS_PROMPT,
    PATIENT_MATCH_PROMPT,
    TEXT_RISK_SUMMARY_PROMPT,
)
from ai_engine.validators.output_validator import parse_ai_json

router = APIRouter()

def _ollama_available() -> bool:
    try:
        return requests.get(settings.OLLAMA_BASE_URL, timeout=2).status_code == 200
    except requests.RequestException:
        return False

def _chat(prompt: str, model: str) -> str:
    import ollama
    client = ollama.Client(host=settings.OLLAMA_BASE_URL)
    response = client.chat(model=model, messages=[{"role": "user", "content": prompt}], format="json")
    return response["message"]["content"]

def _is_quota_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return "429" in msg or "usage limit" in msg or "rate limit" in msg or "quota" in msg

def _chat_with_preference(prompt: str, preference: str = "auto"):
    """
    preference "cloud" -> forces PRIMARY_MODEL, raises if it fails (no silent fallback)
    preference "local" -> forces FALLBACK_MODEL directly, skipping the cloud call entirely
    preference "auto" (default) -> tries PRIMARY_MODEL, and ONLY on a quota/rate-limit
    error automatically retries with FALLBACK_MODEL
    """
    preference = (preference or "auto").lower()

    if preference == "local":
        return _chat(prompt, settings.FALLBACK_MODEL), settings.FALLBACK_MODEL

    if preference == "cloud":
        return _chat(prompt, settings.PRIMARY_MODEL), settings.PRIMARY_MODEL

    try:
        return _chat(prompt, settings.PRIMARY_MODEL), settings.PRIMARY_MODEL
    except Exception as exc:
        if _is_quota_error(exc):
            return _chat(prompt, settings.FALLBACK_MODEL), settings.FALLBACK_MODEL
        raise

@router.get("/status")
def ai_status():
    return {"status": "online" if _ollama_available() else "offline", "model": settings.PRIMARY_MODEL, "fallback_model": settings.FALLBACK_MODEL}

@router.get("/models")
def list_models():
    return {"cloud": settings.PRIMARY_MODEL, "local": settings.FALLBACK_MODEL}

@router.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...), model_preference: str = Form("auto"), db: Session = Depends(get_db)):
    if not _ollama_available():
        raise HTTPException(status_code=503, detail="OLLAMA_OFFLINE")

    text = await extract_text(file)
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in the uploaded file.")

    try:
        raw, model_used = _chat_with_preference(DOCUMENT_ANALYSIS_PROMPT.format(content=text[:10000]), model_preference)
        data = parse_ai_json(raw, required_keys=["summary", "risk_score", "confidence", "structured_data"])
        data.setdefault("visualizations", [])
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI_PROCESS_ERROR: {exc}") from exc

    record = AIAnalysisModel(
        filename=file.filename or "pasted-text.txt",
        created_at=datetime.datetime.utcnow().isoformat() + "Z",
        analysis_json=json.dumps(data),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {"status": "success", "id": record.id, "created_at": record.created_at, "analysis": data, "model_used": model_used}

@router.get("/analyses")
def list_analyses(db: Session = Depends(get_db)):
    records = db.query(AIAnalysisModel).order_by(AIAnalysisModel.id.desc()).all()
    result = []
    for r in records:
        data = json.loads(r.analysis_json)
        result.append({"id": r.id, "filename": r.filename, "created_at": r.created_at, "summary": data.get("summary"), "risk_score": data.get("risk_score"), "confidence": data.get("confidence")})
    return result

@router.get("/analyses/{analysis_id}")
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    record = db.query(AIAnalysisModel).filter(AIAnalysisModel.id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {"id": record.id, "filename": record.filename, "created_at": record.created_at, "analysis": json.loads(record.analysis_json)}

@router.delete("/analyses")
def clear_analyses(db: Session = Depends(get_db)):
    count = db.query(AIAnalysisModel).delete()
    db.commit()
    return {"status": "cleared", "count": count}

@router.delete("/analyses/{analysis_id}")
def delete_analysis(analysis_id: int, db: Session = Depends(get_db)):
    record = db.query(AIAnalysisModel).filter(AIAnalysisModel.id == analysis_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")
    db.delete(record)
    db.commit()
    return {"status": "deleted", "id": analysis_id}

@router.post("/analyze-text")
def analyze_text(payload: TextAnalysisRequest):
    if not _ollama_available():
        raise HTTPException(status_code=503, detail="OLLAMA_OFFLINE")
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="No input provided")
    try:
        raw, model_used = _chat_with_preference(TEXT_RISK_SUMMARY_PROMPT.format(content=payload.text[:5000]), payload.model_preference)
        data = parse_ai_json(raw, required_keys=["summary", "risk_score", "confidence", "risk_analysis"])
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI_PROCESS_ERROR: {exc}") from exc
    return {"status": "success", "analysis": data, "model_used": model_used}

@router.post("/patient-match")
def patient_match(payload: PatientMatchRequest):
    if not _ollama_available():
        raise HTTPException(status_code=503, detail="OLLAMA_OFFLINE")
    try:
        raw, model_used = _chat_with_preference(
            PATIENT_MATCH_PROMPT.format(patient_data=payload.patient_data[:4000], trial_criteria=payload.trial_criteria[:4000]),
            payload.model_preference,
        )
        data = parse_ai_json(raw, required_keys=["match_percentage", "verdict", "reasons"])
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI_PROCESS_ERROR: {exc}") from exc
    return {"status": "success", "match": data, "model_used": model_used}
