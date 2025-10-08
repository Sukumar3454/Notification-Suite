from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
import json, spacy, dateparser
from pathlib import Path

# =========================
# 🔧 SETUP
# =========================
app = FastAPI(
    title="Unified Notification Intelligence API",
    description="Implements F7 (Traceability), F8 (Intelligence), and F9 (Preferences)",
    version="1.0.0"
)

# File paths
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)
NOTIF_FILE = DATA_DIR / "notifications.json"
DETECT_FILE = DATA_DIR / "detections.json"
SETTINGS_FILE = DATA_DIR / "user_settings.json"

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

# =========================
# 📘 UTIL FUNCTIONS
# =========================
def load_json(file_path):
    if file_path.exists():
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# =========================
# F7: TRACEABILITY MODELS
# =========================
VALID_ENTITIES = ["Candidate", "Requirement", "Vendor", "Lead", "Case"]

class NotificationInput(BaseModel):
    entity_type: Literal["Candidate", "Requirement", "Vendor", "Lead", "Case"] = Field(..., example="Case")
    entity_id: int = Field(..., example=123)
    message: str = Field(..., example="New email received")

# =========================
# F8: INTELLIGENCE MODELS
# =========================
class MessageInput(BaseModel):
    text: str = Field(..., example="Let's meet tomorrow at 3pm to discuss updates")

# =========================
# F9: PREFERENCES MODELS
# =========================
class UserSettingsInput(BaseModel):
    user_id: str = Field(..., example="user123")
    muted_notifications: Optional[List[str]] = Field(default=[], example=["marketing", "system_alerts"])
    quiet_hours_start: Optional[str] = Field(default="22:00", example="22:00")
    quiet_hours_end: Optional[str] = Field(default="07:00", example="07:00")
    digest_mode: Optional[bool] = Field(default=False, example=True)

# =========================
# ROUTES: HEALTH CHECK
# =========================
@app.get("/", tags=["Root"])
def root():
    return {"message": "Unified Notification Intelligence API is running (F7, F8, F9)"}

# =========================
# 🧩 F7: TRACEABILITY ENDPOINTS
# =========================
@app.post("/f7/notifications", tags=["F7 - Traceability"])
def create_notification(request: NotificationInput):
    if request.entity_type not in VALID_ENTITIES:
        raise HTTPException(status_code=400, detail="Invalid entity type")

    # Ensure message mentions entity
    message = request.message
    if request.entity_type not in message:
        message = f"{message} on {request.entity_type} {request.entity_id}"

    notification = {
        "entity_type": request.entity_type,
        "entity_id": request.entity_id,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }

    data = load_json(NOTIF_FILE)
    data.append(notification)
    save_json(NOTIF_FILE, data)

    return {"status": "success", "data": notification}

@app.get("/f7/notifications", tags=["F7 - Traceability"])
def get_notifications():
    data = load_json(NOTIF_FILE)
    return {"count": len(data), "data": data}

# =========================
# 🧠 F8: INTELLIGENCE ENDPOINTS
# =========================
@app.post("/f8/detect", tags=["F8 - Intelligence"])
def detect_meeting_deadline(request: MessageInput):
    doc = nlp(request.text)
    detections = []

    for ent in doc.ents:
        if ent.label_ in ["TIME", "DATE"]:
            parsed = dateparser.parse(ent.text)
            if parsed:
                detections.append({
                    "detected_phrase": ent.text,
                    "interpreted_as": parsed.strftime("%Y-%m-%d %H:%M:%S")
                })

    if detections:
        data = load_json(DETECT_FILE)
        data.append({
            "original_text": request.text,
            "detections": detections,
            "timestamp": datetime.now().isoformat()
        })
        save_json(DETECT_FILE, data)
        return {
            "assistive": True,
            "message": "Detected meeting/deadline phrases.",
            "suggestions": ["Add to calendar", "Set a reminder", "Ignore"],
            "detections": detections
        }

    return {
        "assistive": False,
        "message": "No time-related expressions found.",
        "detections": []
    }

@app.get("/f8/detections", tags=["F8 - Intelligence"])
def get_detections():
    data = load_json(DETECT_FILE)
    return {"count": len(data), "data": data}

# =========================
# ⚙️ F9: PREFERENCES ENDPOINTS
# =========================
@app.post("/f9/settings", tags=["F9 - Preferences"])
def create_or_update_user_settings(request: UserSettingsInput):
    data = load_json(SETTINGS_FILE)
    existing = next((item for item in data if item["user_id"] == request.user_id), None)

    settings = {
        "user_id": request.user_id,
        "muted_notifications": request.muted_notifications,
        "quiet_hours_start": request.quiet_hours_start,
        "quiet_hours_end": request.quiet_hours_end,
        "digest_mode": request.digest_mode,
        "updated_at": datetime.now().isoformat()
    }

    if existing:
        data = [item if item["user_id"] != request.user_id else settings for item in data]
        message = "Settings updated successfully"
    else:
        data.append(settings)
        message = "Settings created successfully"

    save_json(SETTINGS_FILE, data)
    return {"status": "success", "message": message, "data": settings}

@app.get("/f9/settings/{user_id}", tags=["F9 - Preferences"])
def get_user_settings(user_id: str):
    data = load_json(SETTINGS_FILE)
    user = next((item for item in data if item["user_id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User settings not found")
    return {"status": "success", "data": user}
