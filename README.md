
# AIIA CTMS 🌿
**AI-Integrated Ayurveda Clinical Trial Management System**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/AI-Ollama%20%2B%20Gemma-orange.svg)](https://ollama.com/)

A specialized dashboard designed for the management of Ayurvedic clinical trials. The system streamlines trial administration, participant enrollment, and pharmacovigilance, while integrating a powerful AI layer (via Ollama and Gemma) to automate the screening of patients against complex trial protocols.

## 🚀 Key Features

### 📋 Trial & Participant Management
*   **End-to-End Trial Tracking:** Create and manage trials with real-time enrollment tracking against target sample sizes.
*   **Participant Enrollment:** Efficiently enroll and filter participants across multiple active trials.
*   **Interoperability:** One-click export of trial data into **CDISC/FHIR `ResearchStudy`** bundles for integration with global health systems.

### 🛡️ Pharmacovigilance (Safety)
*   **Adverse Event Tracking:** Log and monitor adverse events tied directly to participants.
*   **Severity Classification:** Categorize events by severity, including **Serious Adverse Events (SAE)**, with advanced filtering by trial.

### 🤖 AI-Powered Analysis
*   **Automated Protocol Screening:** Upload PDF/CSV/Excel documents to extract summaries, generate risk scores (1–100), and calculate AI confidence levels.
*   **Intelligent Patient Matcher:** Compare patient records against inclusion/exclusion criteria to receive a match percentage, verdict, and detailed reasoning.
*   **Hybrid AI Architecture:** Seamlessly switch between **Cloud-hosted models** (for speed) and **Local Ollama models** (for privacy and unlimited usage) with automatic fallback logic.
*   **Data Visualization:** Auto-generates charts from analysis data and maintains a searchable history of all AI interactions.

---

## 🤖 AI Configuration

**Activating AI Features**
The AI Analyzer, Patient Matcher, and the dashboard's AI risk-insight widget all require **Ollama** to be running locally. 

> [!IMPORTANT]
> If Ollama is not running, the rest of the dashboard will function normally, but AI-specific features will display **"AI Offline."** This is expected behavior, not a bug.

### Setup Steps:
1. **Install Ollama:** Download and install from [ollama.com](https://ollama.com). Ensure it is running (`ollama serve` or as a background service).
2. **Pull the Model:** Download the fallback model to your local machine:
   ```bash
   ollama pull mistral

3.Sync Configuration: Match the model names in your .env file to what is shown in ollama list.
    PRIMARY_MODEL: gemma 4 (Cloud/Primary)
    FALLBACK_MODEL: mistral (Local/Ollama)
Model Selection Logic:
    In the AI Analyzer and Patient Matcher pages, you will find a Model Dropdown:
Auto (Recommended): Tries the Primary/Cloud model first; automatically falls back to Local if the cloud hits a rate limit.
    Cloud only: Forces the use of the Primary model.
    Local only: Forces the use of the local Ollama model.

🛠️ Tech Stack
Layer	Technology
    Backend	Python 3.10+, FastAPI, SQLAlchemy, SQLite, Pydantic
    Authentication	JWT (python-jose, passlib)
    AI Engine	Ollama, Gemma Model, JSON-mode prompt contracts
    Data Processing	Pandas, PyPDF2
    Frontend	Next.js 14, React, TypeScript, Tailwind CSS (or Standalone HTML/JS)


🏁 Getting Started
    Prerequisites
    Python 3.10+
    Node.js 18+ (Optional: only for Next.js frontend)
    Ollama (Required for AI features)

Installation & Setup
1. Backend Configurationgit clone <your-repo-url>
    cd aiia-ctms/backend

# Create and activate virtual environment
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate   # Windows
    pip install -r requirements.txt

2. Environment Setup
   Create a .env file in the backend/ directory:
    SECRET_KEY=***
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=1440
    DEMO_USER_EMAIL=admin@example.com
    DEMO_USER_PASSWORD=***
    OLLAMA_BASE_URL=http://127.0.0.1:11434
    PRIMARY_MODEL=gemma 4
    FALLBACK_MODEL=mistral
   
3. Database Seeding (Optional)
    python ../database/seeds/seed_data.py
4. Launching the System

   Start Backend: uvicorn main:app --reload --port 8000
   Start Frontend (Next.js): cd ../frontend && npm install && npm run dev
   Access Dashboard: Visit http://localhost:3000 (or open index.html for the simple version).

📁 Project Structure
aiia-ctms/
├── backend/
│   ├── main.py               # App entry point
│   ├── aiia_ctms.db          # SQLite Database
│   ├── app/
│   │   ├── core/             # Config & DB connection
│   │   ├── models/           # Data schemas
│   │   └── modules/          # Auth, Trials, Safety, FHIR, AI Service
│   └── tests/                # Pytest suite
├── ai_engine/
│   ├── prompts/              # AI Prompt engineering
│   ├── processing/           # Document extraction logic
│   └── validators/           # JSON output validation
├── database/
│   └── seeds/                # Demo data scripts
└── frontend/
    ├── index.html            # Standalone dashboard
    └── app/                  # Next.js application
    
🧪 Testing
Run the smoke-test suite to verify core functionality:
    cd backend
    pytest tests/ -v

    
