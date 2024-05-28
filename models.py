from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    
    scores = relationship("Score", back_populates="student")

class Score(Base):
    __tablename__ = 'scores'
    
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    student_id = Column(Integer, ForeignKey('students.id'))
    created_at = Column(Date, default=datetime.date.today)
    
    student = relationship("Student", back_populates="scores")
