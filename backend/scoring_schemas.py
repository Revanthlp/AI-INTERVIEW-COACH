from pydantic import BaseModel


class AnswerScoreRequest(BaseModel):
    question: str
    answer: str