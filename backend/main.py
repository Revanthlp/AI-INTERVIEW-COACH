from pathlib import Path
import json

from fastapi import FastAPI

app = FastAPI(title="AI Interview Coach")


BASE_DIR = Path(__file__).resolve().parent.parent
QUESTIONS_FILE = BASE_DIR / "data" / "questions.json"


@app.get("/")
def home():
    return {
        "message": "AI Interview Coach API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/questions")
def get_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        questions = json.load(file)

    return {
        "count": len(questions),
        "questions": questions
    }