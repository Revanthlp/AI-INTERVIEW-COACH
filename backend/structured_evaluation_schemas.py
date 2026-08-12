from pydantic import BaseModel


class StructuredEvaluationRequest(BaseModel):
    question: str
    answer: str