import io
import pandas as pd
import PyPDF2
from fastapi import HTTPException, UploadFile

async def extract_text(file: UploadFile) -> str:
    filename = (file.filename or "").lower()
    raw = await file.read()
    try:
        if filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(io.BytesIO(raw))
            return " ".join(page.extract_text() or "" for page in reader.pages)
        if filename.endswith(".csv"):
            return pd.read_csv(io.BytesIO(raw)).to_string()
        if filename.endswith((".xlsx", ".xls")):
            return pd.read_excel(io.BytesIO(raw)).to_string()
        return raw.decode("utf-8", errors="ignore")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read file: {exc}") from exc
