"""FastAPI router for quiz generator endpoints."""
from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from core.file_extract import extract_text_from_file
from tools.quiz_generator.models import QuizRequest, QuizResponse, QuizSource
from tools.quiz_generator.service import generate

router = APIRouter(prefix="/quiz", tags=["Quiz Generator"])


@router.post("/generate", response_model=QuizResponse)
async def generate_from_text(payload: QuizRequest) -> QuizResponse:
    """Generate quiz from JSON body (topics + text sources)."""
    return generate(payload)


@router.post("/generate-from-files", response_model=QuizResponse)
async def generate_from_files(
    topics: str = Form(...),
    num_questions: int = Form(10, ge=3, le=30),
    difficulty: str = Form("mixed"),
    sources_text: str = Form(""),
    files: Optional[List[UploadFile]] = File(default=None),
) -> QuizResponse:
    """Generate quiz from uploaded PDF/DOCX files and/or pasted text."""
    topic_list = [t.strip() for t in topics.replace(",", "\n").split("\n") if t.strip()]
    if not topic_list:
        raise HTTPException(status_code=400, detail="Add at least one topic.")

    sources: List[QuizSource] = []

    if sources_text.strip():
        sources.append(QuizSource(title="Pasted text", content=sources_text.strip()))

    for f in (files or []):
        if not f.filename:
            continue
        text = await extract_text_from_file(f)
        if text.strip():
            sources.append(QuizSource(title=f.filename, content=text))

    if not sources:
        raise HTTPException(
            status_code=400,
            detail="Provide source material: paste text and/or upload PDF/DOCX.",
        )

    return generate(QuizRequest(
        topics=topic_list,
        sources=sources,
        num_questions=num_questions,
        difficulty=difficulty,
    ))
