# 🚀 Notification Suite – F7, F8, F9

## 📖 Overview
**Notification Suite** is an intelligent FastAPI-based system combining three key modules:

| Feature | Code | Purpose |
|----------|------|----------|
| 🧩 **F7 – Traceability** | `/f7/notifications` | Ensures every notification is linked to a valid entity (`Candidate`, `Vendor`, `Case`, etc.) |
| 🧠 **F8 – Intelligence** | `/f8/detect` | Uses AI to detect meeting/deadline phrases (like “tomorrow 3pm”) and suggest reminders |
| ⚙️ **F9 – Preferences** | `/f9/settings` | Allows users to customize notification behavior — mute, quiet hours, digest mode |

This suite demonstrates **AI-driven traceable notifications** with full **user customization capabilities**, all accessible and testable through **Swagger UI**.

---

## 🧱 Project Structure
notification_suite/
│
├── app/
│ ├── init.py
│ ├── main.py # Unified FastAPI application
│ ├── models.py
│ ├── schemas.py
│ ├── database.py
│
├── data/
│ ├── notifications.json # F7 data
│ ├── detections.json # F8 data
│ └── user_settings.json # F9 data
│
├── F7_README.md
├── F8_README.md
├── F9_README.md
├── requirements.txt
└── README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate

2️⃣ Install Dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

3️⃣ Run FastAPI Application
uvicorn app.main:app --reload

🌐 Open Swagger UI

Go to:
👉 http://127.0.0.1:8000/docs

You’ll see three grouped API sections:

F7 – Traceability

F8 – Intelligence

F9 – Preferences

Each can be tested directly from Swagger.

🧩 API Overview
🧩 F7 – Traceability Notification

POST /f7/notifications

{
  "entity_type": "Case",
  "entity_id": 123,
  "message": "New email received"
}


✅ Response:

{
  "status": "success",
  "data": {
    "entity_type": "Case",
    "entity_id": 123,
    "message": "New email received on Case 123",
    "timestamp": "2025-10-07T12:45:00"
  }
}


🗂 Data saved to: data/notifications.json

🧠 F8 – Intelligence (Detect Meetings / Deadlines)

POST /f8/detect

{
  "text": "Let's meet tomorrow at 3pm to finalize the proposal"
}


✅ Response:

{
  "assistive": true,
  "message": "Detected meeting/deadline phrases.",
  "suggestions": ["Add to calendar", "Set a reminder", "Ignore"],
  "detections": [
    {
      "detected_phrase": "tomorrow at 3pm",
      "interpreted_as": "2025-10-08 15:00:00"
    }
  ]
}


🗂 Data saved to: data/detections.json

⚙️ F9 – Preferences (User Settings)

POST /f9/settings

{
  "user_id": "user123",
  "muted_notifications": ["marketing", "system_alerts"],
  "quiet_hours_start": "22:00",
  "quiet_hours_end": "07:00",
  "digest_mode": true
}


✅ Response:

{
  "status": "success",
  "message": "Settings created successfully",
  "data": {
    "user_id": "user123",
    "muted_notifications": ["marketing", "system_alerts"],
    "quiet_hours_start": "22:00",
    "quiet_hours_end": "07:00",
    "digest_mode": true,
    "updated_at": "2025-10-07T22:50:00"
  }
}


🗂 Data saved to: data/user_settings.json

✅ Successful Swagger Confirmation
Module	Success Key in Swagger Response
F7 – Traceability	"status": "success"
F8 – Intelligence	"assistive": true"
F9 – Preferences	"status": "success"

Once all three show these success responses, your Notification Suite is working perfectly.

📚 Individual Documentation
Module	File	Description
F7	F7_README.md
	Traceability Notification API setup & test
F8	F8_README.md
	Intelligence API setup & test
F9	F9_README.md
	Preferences API setup & test
🧠 Summary

This Notification Suite provides:

✅ Traceability (F7): Enforces entity-linked notifications.

🤖 Intelligence (F8): Detects time expressions and assists with reminders.

⚙️ Preferences (F9): Enables user-controlled notification customization.

All features are independent yet seamlessly integrated into one unified FastAPI system.

🏁 Author

Developed by: Sukumar (Quadrant Technologies)
Stack: Python, FastAPI, spaCy, JSON Storage
Goal: Intelligent, traceable, and customizable notification system.

🧩 Future Enhancements

🔔 Integrate F9 settings to dynamically mute F7 notifications.

📅 Connect F8 reminders with external calendars (Google, Outlook).

📊 Add dashboard and analytics view for notifications.

🎉 Ready to Test

Run:

uvicorn app.main:app --reload


Then open Swagger:
👉 http://127.0.0.1:8000/docs

Test all three modules — and you’re done! ✅
