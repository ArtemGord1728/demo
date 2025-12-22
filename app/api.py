import os
import shutil
import logging
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import FileResponse

from database import engine, get_db, Base
from models import Document
from schemas import DocumentResponse
from service import summarize_pdf

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PDF Summary AI")

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    safe_filename = os.path.basename(filename)
    file_path = UPLOAD_DIR / safe_filename

    if file_path.exists() and file_path.is_file():
        return FileResponse(path=file_path, media_type="audio/mpeg", filename=safe_filename)
    else:
        raise HTTPException(status_code=404, detail="Audio file not found")


@app.post("/upload", response_model=DocumentResponse)
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    safe_filename = os.path.basename(file.filename)
    file_path = UPLOAD_DIR / safe_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result_data = summarize_pdf(str(file_path))

        db_doc = Document(
            filename=safe_filename,
            summary=result_data["text"],
            tokens_used=result_data["tokens"],
            cost_usd=result_data["cost"]
        )
        db.add(db_doc)
        db.commit()
        db.refresh(db_doc)

        return DocumentResponse(
            id=db_doc.id,
            filename=db_doc.filename,
            summary=db_doc.summary,
            tokens_used=db_doc.tokens_used,
            cost_usd=db_doc.cost_usd,
            created_at=db_doc.created_at,
            audio_filename=result_data.get("audio_filename")
        )

    except Exception as e:
        logger.error(f"Error processing file {safe_filename}: {e}", exc_info=True)
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        if file_path.exists():
            os.remove(file_path)

@app.get("/history", response_model=List[DocumentResponse])
def get_history(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.created_at.desc()).limit(5).all()