from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from .student import Student, get_db


# Pydantic Student model
class StudentCreate(BaseModel):
    name: str
    age: int
    email: str

class StudentRead(StudentCreate):
    id: int
    class Config:
        orm_mode = True

app = FastAPI()

@app.post("/students/", response_model=StudentRead)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# /students/?skip=20&limit=50
# Existing paginated endpoint
@app.get("/students/", response_model=List[StudentRead])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students

# New endpoint to return all students without pagination
@app.get("/students/all", response_model=List[StudentRead])
def read_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@app.get("/students/{student_id}", response_model=StudentRead)
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"ok": True}
