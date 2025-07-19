from pydantic import BaseModel

# Pydantic Student model
class StudentCreate(BaseModel):
    name: str
    age: int
    email: str

class StudentRead(StudentCreate):
    id: int
    class Config:
       from_attributes = True