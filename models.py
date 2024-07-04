from pydantic import BaseModel

class Vacancy(BaseModel):
    id: int
    title: str
    experience: str
    salary: str

