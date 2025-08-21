
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageDraw
import pytesseract
import io
import re
import cv2
import numpy as np

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

import spacy
nlp = spacy.load("en_core_web_sm")

PII_PATTERNS = {
    'aadhaar': r'(?:(?:\d[\s-]*){12})',
    'pan': r'\b[A-Z]{5}\d{4}[A-Z]{1}\b',
    'passport': r'\b[A-Z]{1}\d{7}\b',
    'voterid': r'\b[A-Z]{3}\d{7}\b',
    'long_number': r'\b\d{8,}\b',
    'phone': r'\b[6-9]\d{9}\b',
    'email': r'[\w\.-]+@[\w\.-]+',
    'dob': r'\b\d{2}/\d{2}/\d{4}\b',
    'dob_hindi': r'जन्म तिथि|डीओबी',
    'address_hindi': r'पता|गांव|जिला|पोस्ट|तहसील',
}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    # Use Tesseract with English only
    text = pytesseract.image_to_string(image, lang='eng')
    boxes = pytesseract.image_to_data(image, lang='eng', output_type=pytesseract.Output.DICT)

    draw = ImageDraw.Draw(image)
    masked_indices = set()


    # Detect and mask faces using OpenCV Haar Cascade
    cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(cv_img, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    for (x, y, w, h) in faces:
        draw.rectangle([x, y, x+w, y+h], fill='black')


    # Improved Aadhaar masking: check for 12-digit sequences across consecutive words
    words = boxes['text']
    n = len(words)
    for i in range(n):
        # Check single word for 12 digits
        if words[i] and re.fullmatch(r'(?:\d[\s-]*){12}', words[i].replace(' ', '').replace('-', '')):
            if i not in masked_indices:
                x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
                draw.rectangle([x, y, x+w, y+h], fill='black')
                masked_indices.add(i)
        # Check group of 3 consecutive words for 12 digits
        if i+2 < n:
            combined = ''.join([w.replace(' ', '').replace('-', '') for w in words[i:i+3] if w])
            if re.fullmatch(r'\d{12}', combined):
                for j in range(i, i+3):
                    if j not in masked_indices:
                        x, y, w, h = boxes['left'][j], boxes['top'][j], boxes['width'][j], boxes['height'][j]
                        draw.rectangle([x, y, x+w, y+h], fill='black')
                        masked_indices.add(j)

    # Detect PII in OCR text (regex-based, Hindi + English)
    for key, pattern in PII_PATTERNS.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            pii = match.group()
            for i, word in enumerate(boxes['text']):
                if word and (pii in word or re.search(pattern, word, re.IGNORECASE)) and i not in masked_indices:
                    x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
                    draw.rectangle([x, y, x+w, y+h], fill='black')
                    masked_indices.add(i)

    # Detect Full Name and Address using SpaCy NER
    doc = nlp(text)
    person_names = set()
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            person_names.add(ent.text)
        elif ent.label_ in ["GPE", "ORG"]:
            # Mask addresses/orgs as before
            name_or_address = ent.text
            for i, word in enumerate(boxes['text']):
                if word and name_or_address in word and i not in masked_indices:
                    x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
                    draw.rectangle([x, y, x+w, y+h], fill='black')
                    masked_indices.add(i)

    # Mask all SpaCy PERSON entities
    for name in person_names:
        for i, word in enumerate(boxes['text']):
            if word and name in word and i not in masked_indices:
                x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
                draw.rectangle([x, y, x+w, y+h], fill='black')
                masked_indices.add(i)

    # Fallback: Mask capitalized words not matching known keywords (possible names)
    keywords = set(['address', 'dob', 'date', 'of', 'birth', 'father', 'mother', 'post', 'village', 'tehsil', 'district', 'unique', 'identification', 'authority', 'india', 'government', 'male', 'female'])
    for i, word in enumerate(boxes['text']):
        if word and word[0].isupper() and word.lower() not in keywords and i not in masked_indices:
            # Avoid masking numbers and short words
            if not word.isdigit() and len(word) > 2:
                x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
                draw.rectangle([x, y, x+w, y+h], fill='black')
                masked_indices.add(i)

    # Mask specific Hindi name (example)
    hindi_name = 'सखी बाई कुशवाह'
    for i, word in enumerate(boxes['text']):
        if word and hindi_name in word and i not in masked_indices:
            x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
            draw.rectangle([x, y, x+w, y+h], fill='black')
            masked_indices.add(i)

    # Mask address block: mask lines after address-related keywords
    address_keywords = ['address', 'post', 'village', 'tehsil', 'district']
    address_indices = []
    for i, word in enumerate(boxes['text']):
        if word and any(kw in word.lower() for kw in address_keywords):
            address_indices.append(i)

    # Mask the next few lines after address keywords (e.g., up to 5 lines)
    for idx in address_indices:
        for offset in range(0, 6):
            i = idx + offset
            if i < len(boxes['text']) and i not in masked_indices:
                x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
                draw.rectangle([x, y, x+w, y+h], fill='black')
                masked_indices.add(i)

    # Determine original format and filename
    orig_format = image.format if image.format else 'PNG'
    ext = orig_format.lower() if orig_format else 'png'
    orig_name = getattr(file, 'filename', 'masked_image')
    if '.' in orig_name:
        base_name = orig_name.rsplit('.', 1)[0]
    else:
        base_name = orig_name
    masked_filename = f"{base_name}_masked.{ext}"

    buf = io.BytesIO()
    image.save(buf, format=orig_format)
    buf.seek(0)
    headers = {
        "Content-Disposition": f"attachment; filename={masked_filename}"
    }
    return StreamingResponse(buf, media_type=f"image/{ext}", headers=headers)
