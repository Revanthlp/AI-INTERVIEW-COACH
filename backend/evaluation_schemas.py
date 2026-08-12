from pydantic import BaseModel


class AnswerEvaluationRequest(BaseModel):
    question: str
    answer: str