import json

SEED_DATA = {
    "trials": [
        {
            "id": 1, 
            "title": "Ashwagandha for Chronic Stress", 
            "protocol_number": "AYU-2026-001", 
            "ctri_id": "CTRI/AAA-2026/123",
            "status": "Active", 
            "enrollment": 65, 
            "target_sample_size": 100,
            "phase": "Phase II",
            "sponsor": "AIIA Research Wing"
        },
        {
            "id": 2, 
            "title": "Triphala in Type 2 Diabetes", 
            "protocol_number": "AYU-2026-002", 
            "ctri_id": "Pending",
            "status": "Ethics Review", 
            "enrollment": 0, 
            "target_sample_size": 150,
            "phase": "Phase III",
            "sponsor": "National Ayurveda Council"
        },
        {
            "id": 3, 
            "title": "Brahmi for Cognitive Enhancement", 
            "protocol_number": "AYU-2026-003", 
            "ctri_id": "CTRI/AAA-2026/456",
            "status": "Completed", 
            "enrollment": 80, 
            "target_sample_size": 80,
            "phase": "Phase I",
            "sponsor": "AIIA Research Wing"
        }
    ],
    "participants": [
        {"id": 1, "trial_id": 1, "participant_code": "SUBJ-001", "status": "Enrolled", "consent": True},
        {"id": 2, "trial_id": 1, "participant_code": "SUBJ-002", "status": "Withdrawn", "consent": True},
        {"id": 3, "trial_id": 1, "participant_code": "SUBJ-003", "status": "Enrolled", "consent": True},
    ],
    "safety_events": [
        {"id": 1, "participant_id": 1, "description": "Mild insomnia", "severity": "Mild", "causality": "Possibly Related"},
        {"id": 2, "participant_id": 3, "description": "Gastrointestinal upset", "severity": "Moderate", "causality": "Related"},
    ],
    "regulatory_logs": [
        {"id": 1, "trial_id": 1, "event": "Ethics Approval Granted", "date": "2026-01-15"},
        {"id": 2, "trial_id": 2, "event": "Protocol Submitted to EC", "date": "2026-05-10"},
    ]
}

def seed_db():
    with open("db.json", "w") as f:
        json.dump(SEED_DATA, f, indent=4)
    print("✅ AIIA Ayurveda Clinical Data Seeded Successfully!")

if __name__ == "__main__":
    seed_db()
