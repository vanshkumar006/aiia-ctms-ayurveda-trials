from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
import app.core.db_models  # noqa: F401
from app.modules.ai_service.router import router as ai_router
from app.modules.auth.router import router as auth_router
from app.modules.fhir.router import router as fhir_router
from app.modules.participants.router import router as participants_router
from app.modules.regulatory.router import router as regulatory_router
from app.modules.safety.router import router as safety_router
from app.modules.trials.router import router as trials_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="A real-time, cloud-based, GCP-compliant CTMS for Ayurveda research.",
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(trials_router, prefix="/api/trials", tags=["trials"])
app.include_router(participants_router, prefix="/api/participants", tags=["participants"])
app.include_router(safety_router, prefix="/api/safety", tags=["safety"])
app.include_router(regulatory_router, prefix="/api/regulatory", tags=["regulatory"])
app.include_router(fhir_router, prefix="/api/fhir", tags=["fhir"])
app.include_router(ai_router, prefix="/api/ai", tags=["ai"])

@app.get("/")
def root():
    return {"status": "AIIA SYSTEM ONLINE", "version": settings.APP_VERSION}
