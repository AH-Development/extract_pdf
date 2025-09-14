from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from pydantic import BaseModel
import base64
import io

app = FastAPI()

# Autoriser toutes les origines (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-text/")
async def extract_text(file: UploadFile = File(...)):
    """Upload via multipart/form-data"""
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return {"text": text}


# ---- NOUVEL ENDPOINT BASE64 ----
class FilePayload(BaseModel):
    file: str  # base64 string

@app.post("/extract-text-base64/")
async def extract_text_base64(payload: FilePayload):
    """Upload via JSON base64 (utile pour Power Automate HTTP standard)"""
    try:
        # Décoder le base64
        pdf_bytes = base64.b64decode(payload.file)
        pdf_stream = io.BytesIO(pdf_bytes)

        # Lire le PDF
        reader = PdfReader(pdf_stream)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return {"text": text}

    except Exception as e:
        return {"error": str(e)}
