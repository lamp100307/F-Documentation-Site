__all__ = ['Question', 'Answer']

from pydantic import BaseModel
class Question(BaseModel):
    name: str
    question: str

class Answer(Question):
    msg: str
