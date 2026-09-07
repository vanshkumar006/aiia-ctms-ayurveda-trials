DOCUMENT_ANALYSIS_PROMPT = (
    "You are a Medical Research Expert. Analyze the following clinical data and "
    "return ONLY a raw JSON object. The JSON MUST contain exactly these keys: "
    "1. 'summary': (a brief overview, 2-3 sentences) "
    "2. 'risk_score': (a number from 1-100) "
    "3. 'confidence': (a number from 0-100 representing how confident you are in this "
    "analysis, lower if the data is incomplete, ambiguous, or too short to analyze reliably) "
    "4. 'structured_data': (an object containing 'sample_size', 'phase', 'inclusion_criteria', "
    "and 'exclusion_criteria') "
    "5. 'visualizations': (a list of 0-3 chart specs, ONLY if the data contains categorical or "
    "numeric columns worth visualizing, e.g. patient counts by diagnosis or department. Each item "
    "must be an object with: 'title' (short string), 'type' ('bar' or 'pie'), 'labels' (list of "
    "category names), and 'values' (list of numbers, same length as labels). Return an empty list "
    "[] if nothing is worth charting.) "
    "DATA: {content}"
)

TEXT_RISK_SUMMARY_PROMPT = (
    "You are a clinical trial risk monitor. Given the trial data below, return ONLY "
    "a raw JSON object with exactly these keys: "
    "1. 'summary': (one sentence, overall status) "
    "2. 'risk_score': (a number from 1-100) "
    "3. 'confidence': (a number from 0-100 for how confident you are in this assessment) "
    "4. 'risk_analysis': (2-3 sentences on the most notable risk or trend) "
    "DATA: {content}"
)

PATIENT_MATCH_PROMPT = (
    "You are a clinical trial eligibility screener. Compare the patient record to the "
    "trial criteria and return ONLY a raw JSON object with exactly these keys: "
    "1. 'match_percentage': (a number from 0-100) "
    "2. 'verdict': (one of 'Eligible', 'Likely Eligible', 'Likely Ineligible', 'Ineligible') "
    "3. 'reasons': (a list of short strings explaining the verdict) "
    "PATIENT DATA: {patient_data} "
    "TRIAL CRITERIA: {trial_criteria}"
)
