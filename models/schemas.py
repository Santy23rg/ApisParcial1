from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from database.connection import Base

# ---------------- Pydantic Models ----------------

# Students
class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(...)

class Student(StudentBase):
    id: int
    created_at: datetime
    is_active: bool = True
    class Config:
        from_attributes = True

class StudentResponse(BaseModel):
    message: str
    student: Optional[Student] = None


# Teachers
class TeacherBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    subject: str = Field(..., max_length=100)

class Teacher(TeacherBase):
    id: int
    created_at: datetime
    is_active: bool = True
    class Config:
        from_attributes = True

class TeacherResponse(BaseModel):
    message: str
    teacher: Optional[Teacher] = None


# Subjects
class SubjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    credits: int = Field(..., ge=1, le=10)

class Subject(SubjectBase):
    id: int
    created_at: datetime
    is_active: bool = True
    class Config:
        from_attributes = True

class SubjectResponse(BaseModel):
    message: str
    subject: Optional[Subject] = None


# Notes
class NoteBase(BaseModel):
    student_id: int
    subject_id: int
    grade: float = Field(..., ge=0, le=5)

class Note(NoteBase):
    id: int
    created_at: datetime
    is_active: bool = True
    class Config:
        from_attributes = True

class NoteResponse(BaseModel):
    message: str
    note: Optional[Note] = None


# ---------------- SQLAlchemy Models ----------------

class StudentDB(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class TeacherDB(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    subject = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class SubjectDB(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    credits = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class NoteDB(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    grade = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
