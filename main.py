from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import datetime

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class StudentCreate(BaseModel):
    name: str
    age: int

class StudentUpdate(BaseModel):
    name: str
    age: int

class ScoreCreate(BaseModel):
    score: int
    student_id: int
    created_at: Optional[datetime.date] = None

class ScoreUpdate(BaseModel):
    score: int

class ScoreGet(BaseModel):
    id: int
    score: int
    created_at: datetime.date

    class Config:
        orm_mode = True

class StudentScoresGet(BaseModel):
    id: int
    name: str
    age: int
    scores: List[ScoreGet]

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD для учеников

@app.post("/students/", response_model=StudentCreate)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(name=student.name, age=student.age)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/students")
def read_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students

@app.get("/students/{student_id}/scores", response_model=StudentScoresGet)
def read_student_scores(
    student_id: int, 
    db: Session = Depends(get_db),
    start_date: Optional[datetime.date] = Query(None),
    end_date: Optional[datetime.date] = Query(None)
):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    query = db.query(models.Score).filter(models.Score.student_id == student_id)
    
    if start_date:
        query = query.filter(models.Score.created_at >= start_date)
    if end_date:
        query = query.filter(models.Score.created_at <= end_date)
    
    scores = query.all()
    
    return StudentScoresGet(
        id=student.id,
        name=student.name,
        age=student.age,
        scores=[ScoreGet(id=score.id, score=score.score, created_at=score.created_at) for score in scores]
    )

@app.patch("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.name = student.name
    db_student.age = student.age
    db.commit()
    db.refresh(db_student)
    return db_student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}

# CRUD для оценок

@app.post("/scores/", response_model=ScoreGet)
def create_score(score: ScoreCreate, db: Session = Depends(get_db)):
    if score.created_at is None:
        score.created_at = datetime.date.today()
    elif score.created_at > datetime.date.today():
        raise HTTPException(status_code=400, detail="created_at cannot be in the future")

    db_score = models.Score(score=score.score, student_id=score.student_id, created_at=score.created_at)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

@app.get("/scores/{score_id}", response_model=ScoreGet)
def read_score(score_id: int, db: Session = Depends(get_db)):
    score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    return score

@app.patch("/scores/{score_id}", response_model=ScoreGet)
def update_score(score_id: int, score: ScoreUpdate, db: Session = Depends(get_db)):
    db_score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if db_score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    db_score.score = score.score
    db.commit()
    db.refresh(db_score)
    return db_score

@app.delete("/scores/{score_id}")
def delete_score(score_id: int, db: Session = Depends(get_db)):
    db_score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if db_score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    db.delete(db_score)
    db.commit()
    return {"message": "Score deleted successfully"}
