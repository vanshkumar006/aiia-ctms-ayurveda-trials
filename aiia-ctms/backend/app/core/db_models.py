from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Trial(Base):
    __tablename__ = "trials"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(String, default="Ethics Review")
    enrollment = Column(Integer, default=0)
    ctri_id = Column(String, default="Pending")
    target_sample_size = Column(Integer, default=100)
    protocol_number = Column(String, nullable=True)
    phase = Column(String, nullable=True)
    sponsor = Column(String, nullable=True)
    participants = relationship("Participant", back_populates="trial", cascade="all, delete-orphan")
    regulatory_logs = relationship("RegulatoryLog", back_populates="trial", cascade="all, delete-orphan")

class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    trial_id = Column(Integer, ForeignKey("trials.id"), nullable=False)
    participant_code = Column(String, nullable=False)
    status = Column(String, default="Enrolled")
    consent = Column(Boolean, default=True)
    trial = relationship("Trial", back_populates="participants")
    safety_events = relationship("SafetyEvent", back_populates="participant", cascade="all, delete-orphan")

class SafetyEvent(Base):
    __tablename__ = "safety_events"
    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    description = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    causality = Column(String, nullable=False)
    participant = relationship("Participant", back_populates="safety_events")

class RegulatoryLog(Base):
    __tablename__ = "regulatory_logs"
    id = Column(Integer, primary_key=True, index=True)
    trial_id = Column(Integer, ForeignKey("trials.id"), nullable=False)
    event = Column(String, nullable=False)
    date = Column(String, nullable=False)
    trial = relationship("Trial", back_populates="regulatory_logs")

class AIAnalysis(Base):
    __tablename__ = "ai_analyses"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    analysis_json = Column(Text, nullable=False)
