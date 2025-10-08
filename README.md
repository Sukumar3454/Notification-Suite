# 🧩 Unified Notification Intelligence API (F7 + F8 + F9)

## Overview
This FastAPI app combines:
- **F7 (Traceability):** Every notification must link to a valid entity.
- **F8 (Intelligence):** Detect meeting/deadline words in messages and suggest reminders.
- **F9 (Preferences):** Manage per-user notification settings (mute, quiet hours, digest mode).

---

## ⚙️ Setup
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload
