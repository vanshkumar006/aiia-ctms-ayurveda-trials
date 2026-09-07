from fastapi import APIRouter, HTTPException, UploadFile, File
import ollama
import pandas as pd
import PyPDF2
import io
import requests
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import re

router = APIRouter()

# Standard Local Loopback
OLLAMA_URL = "http://127.0.0.1:11434"
MODEL_NAME = "gemma4:31b-cloud"

def test_ollama_connection():
    try:
        response = requests.get(f"{OLLAMA_URL}", timeout=2)
        return response.status_code == 200
    except Exception:
        return False

async def process_pdf(file: UploadFile):
    try:
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF Error: {str(e)}")

async def process_csv_excel(file: UploadFile):
    try:
        content = await file.read()
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
        return df.to_string()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Table Error: {str(e)}")

def clean_json_output(text: str) -> str:
    # Remove Markdown code blocks
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s*```$', '', text, flags=re.MULTILINE)
    # Handle potential leading/trailing non-JSON text
    start_index = text.find('{')
    end_index = text.rfind('}')
    if start_index != -1 and end_index != -1:
        text = text[start_index:end_index+1]
    return text.strip()

@router.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    if not test_ollama_connection():
        raise HTTPException(status_code=503, detail="OLLAMA_OFFLINE")

    try:
        if file.filename.endswith('.pdf'):
            text = await process_pdf(file)
        elif file.filename.endswith(('.csv', '.xlsx', '.xls')):
            text = await process_csv_excel(file)
        else:
            content = await file.read()
            text = content.decode('utf-8')

        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="No readable text found.")

        # STRENGTHENED PROMPT: Forcing specific JSON keys
        prompt = (
            "You are a Medical Research Expert. Analyze the following clinical data and return ONLY a raw JSON object. "
            "The JSON MUST contain exactly these keys: "
            "1. 'summary': (A brief overview) "
            "2. 'risk_score': (A number from 1-100) "
            "3. 'structured_data': (An object containing 'sample_size', 'phase', 'inclusion_criteria', and 'exclusion_criteria') "
            f"DATA: {text[:10000]}"
        )
        
        client = ollama.Client(host=OLLAMA_URL)
        response = client.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            format="json"
        )
        
        raw_content = response['message']['content']
        cleaned_json = clean_json_output(raw_content)
        
        # Final verification
        try:
            json.loads(cleaned_json)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="AI returned malformed JSON. Please try again.")

        return {"status": "success", "analysis": cleaned_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI_PROCESS_ERROR: {str(e)}")
