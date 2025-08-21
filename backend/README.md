# Backend: PII Masking API

## Features
- Accepts image uploads via `/upload` endpoint
- Extracts text using OCR (Tesseract)
- Detects PII (Aadhaar, phone, email, DOB) using regex
- Masks/redacts detected PII directly on the image
- Returns the masked image

## How to Run

1. Install dependencies:
   ```powershell
   "C:/Users/Hey Buddy/Desktop/mindcraft lab/.venv/Scripts/python.exe" -m pip install -r requirements.txt
   ```
2. Start the server:
   ```powershell
   "C:/Users/Hey Buddy/Desktop/mindcraft lab/.venv/Scripts/python.exe" -m uvicorn main:app --reload
   ```
3. Test the API at `http://127.0.0.1:8000/docs`

## API Usage
- POST `/upload` with an image file (form-data, key: `file`)
- Receives masked image in response

---
Next: Frontend React app for image upload and display.
