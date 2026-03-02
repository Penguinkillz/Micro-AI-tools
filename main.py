"""
Platform entry point.

Each tool registers its own router here.
To add a new tool:
  1. Create tools/<tool_name>/router.py
  2. Import its router and add app.include_router() below.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from tools.quiz_generator.router import router as quiz_router

app = FastAPI(title="AI Tools Platform", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register tool routers ---
app.include_router(quiz_router, prefix="/api")

# --- Serve quiz generator frontend as default UI ---
app.mount("/", StaticFiles(directory="tools/quiz_generator/frontend", html=True), name="frontend")
