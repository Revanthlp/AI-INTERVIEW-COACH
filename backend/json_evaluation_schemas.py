from pydantic import BaseModel
from typing import List


class JSONEvaluationRequest(BaseModel):
    question: str
    answer: str


class JSONEvaluationResponse(BaseModel):
    overall_score: int
    correctness: int
    relevance: int
    clarity: int
    completeness: int
    strengths: List[str]
    improvements: List[str]
    better_answer: str