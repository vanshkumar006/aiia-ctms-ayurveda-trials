import json
import re
from typing import Any, Dict

def clean_json_output(text: str) -> str:
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end + 1]
    return text.strip()

def parse_ai_json(raw_content: str, required_keys):
    cleaned = clean_json_output(raw_content)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(f"AI returned malformed JSON: {exc}") from exc
    missing = [k for k in required_keys if k not in data]
    if missing:
        raise ValueError(f"AI response missing expected keys: {missing}")
    return data
