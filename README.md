# Mindcraft Lab: PII Masking API

## Project Overview

This project is a backend API built with **FastAPI** that enables secure handling of sensitive information in images. The API allows users to upload images, automatically extracts text using OCR (Optical Character Recognition), detects Personally Identifiable Information (PII) such as Aadhaar numbers, phone numbers, email addresses, and dates of birth, and masks/redacts these PII elements directly on the image. The processed image is then returned to the user, ensuring privacy and compliance.

## Key Features

- **Image Upload:** Accept images via a simple API endpoint.
- **OCR Integration:** Uses Tesseract OCR to extract text from images.
- **PII Detection:** Identifies Aadhaar numbers, phone numbers, emails, and DOBs using regular expressions.
- **PII Masking:** Redacts detected PII directly on the image for privacy.
- **API Response:** Returns the masked image to the user.

## Technologies Used

- **FastAPI:** High-performance Python web framework for building APIs.
- **Tesseract OCR:** Open-source OCR engine for text extraction.
- **Pillow:** Python Imaging Library for image processing.
- **Regex:** For pattern-based PII detection.

## How It Works

1. **User uploads an image** containing text via the `/upload` endpoint.
2. **OCR extracts text** from the image.
3. **Regex patterns detect PII** within the extracted text.
4. **PII is masked/redacted** on the image using Pillow.
5. **Masked image is returned** to the user.

## Getting Started

### Prerequisites

- Python 3.8+
- Tesseract OCR installed on your system
- Virtual environment (recommended)

### Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/snsharma0714/Mindcraftlab.git
   cd Mindcraftlab/backend
   ```

2. **Set up a virtual environment:**
   ```
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Ensure Tesseract is installed:**
   - Download from: https://github.com/tesseract-ocr/tesseract
   - Add Tesseract to your system PATH.

### Running the API

Start the FastAPI server:
```
uvicorn main:app --reload
```
Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

### API Usage

- **Endpoint:** `POST /upload`
- **Request:** Form-data with key `file` (image file)
- **Response:** Masked image file

### Example Workflow

1. Open the API docs in your browser.
2. Use the `/upload` endpoint to select and upload an image.
3. Receive the processed image with PII masked.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or new features.

## License

This project is licensed under the MIT License.

---

**Next Steps:**  
A frontend React app will be developed to provide a user-friendly interface for image upload and display of masked results.
