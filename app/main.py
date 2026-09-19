import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'retrieval'))

import logging
from generate import answer
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("github-api-copilot")

app = FastAPI(title="GitHub API Copilot")

# --- Rate limiting: caps requests per IP so no one can burn your free API quota ---
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS: adjust allow_origins to your actual deployed frontend domain once you know it ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TODO: replace "*" with your deployed URL before going public
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class Query(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)

    @field_validator("question")
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Question cannot be empty or whitespace.")
        return v


@app.post("/query")
@limiter.limit("10/minute")   # adjust as needed once you see real usage patterns
def query(request: Request, q: Query):
    try:
        return answer(q.question)
    except Exception as e:
        # Never leak internal stack traces / raw error strings to the client.
        logger.exception(f"Failed to answer question: {q.question!r}")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating an answer. Please try again.",
        )


@app.get("/health")
def health():
    return {"status": "ok"}


app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def root():
    return FileResponse("app/static/index.html")