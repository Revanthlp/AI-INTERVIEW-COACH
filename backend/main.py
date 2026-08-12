from pathlib import Path
import json

from fastapi import FastAPI

from backend.schemas import QuestionRequest
from backend.evaluation_schemas import AnswerEvaluationRequest
from backend.scoring_schemas import AnswerScoreRequest
from backend.ai_engine import (
    generate_answer,
    evaluate_answer,
    score_answer,
)


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


@app.post("/answer")
def answer_question(request: QuestionRequest):
    answer = generate_answer(request.question)

    return {
        "question": request.question,
        "answer": answer
    }


@app.post("/evaluate")
def evaluate_candidate_answer(
    request: AnswerEvaluationRequest
):
    evaluation = evaluate_answer(
        request.question,
        request.answer
    )

    return {
        "question": request.question,
        "answer": request.answer,
        "evaluation": evaluation
    }


@app.post("/score")
def score_candidate_answer(
    request: AnswerScoreRequest
):
    score = score_answer(
        request.question,
        request.answer
    )

    return {
        "question": request.question,
        "answer": request.answer,
        "score": score
    }