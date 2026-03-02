# Micro AI Tools

A growing portfolio of focused AI tools — each solving one real-world problem.
Built with FastAPI + Groq (free tier). New tools are added as modules; no separate backends.

## Live tools

| Tool | Description | Status |
|------|-------------|--------|
| Quiz Generator | Turn notes/PDFs into MCQ quizzes | Live |

## Local setup

### Prerequisites
- Python 3.10+
- A free [Groq API key](https://console.groq.com/)

### Steps

```bash
git clone https://github.com/Penguinkillz/Micro-AI-tools.git
cd Micro-AI-tools

python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the project root (copy from `.env.example`):

```
PLATFORM_GROQ_API_KEY=your_groq_key_here
```

Run the server:

```bash
python -m uvicorn main:app --reload --port 8000
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Project structure

```
Micro-AI-tools/
├── main.py                   ← registers all tool routers
├── core/
│   ├── config.py             ← shared env vars (PLATFORM_ prefix)
│   ├── llm.py                ← shared LLM client + key rotation
│   └── file_extract.py       ← shared PDF/DOCX extraction
├── tools/
│   └── quiz_generator/       ← Tool 1
│       ├── models.py
│       ├── service.py
│       ├── router.py
│       └── frontend/
├── requirements.txt
├── Procfile                  ← Railway deployment
└── .env.example
```

---

## Adding a new tool

1. Create `tools/<tool_name>/` with these files:

```
tools/your_tool/
├── __init__.py
├── models.py       ← Pydantic request/response models
├── service.py      ← business logic, calls get_llm_client()
├── router.py       ← FastAPI APIRouter with endpoints
└── frontend/
    ├── index.html
    └── main.js
```

2. Register it in `main.py`:

```python
from tools.your_tool.router import router as your_tool_router
app.include_router(your_tool_router, prefix="/api")
```

3. That's it. The tool is live on the same deployment.

---

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PLATFORM_GROQ_API_KEY` | Yes | Primary LLM key (Groq free tier) |
| `PLATFORM_GROQ_API_KEY_2` | No | Second key for rotation |
| `PLATFORM_GROQ_API_KEY_3` | No | Third key for rotation |
| `PLATFORM_OPENAI_API_KEY` | No | OpenAI fallback |

---

## Tech stack

- **Backend:** Python, FastAPI
- **LLM:** Groq (Llama 3.3 70B) / OpenAI fallback
- **File parsing:** pypdf, python-docx
- **Deployment:** Railway
- **Analytics:** Umami
