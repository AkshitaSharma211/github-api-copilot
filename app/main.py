import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'retrieval'))
from generate import answer
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/query")
def query(q: Query):
    return answer(q.question)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")