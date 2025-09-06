from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.connection import SessionLocal
from models.schemas import StudentDB, StudentBase, StudentResponse, Student

router = APIRouter(prefix="/students", tags=["Estudiantes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Student])
def get_students(db: Session = Depends(get_db)):
    stmt = select(StudentDB).where(StudentDB.is_active == True)
    return db.execute(stmt).scalars().all()

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentBase, db: Session = Depends(get_db)):
    exists = db.execute(select(StudentDB).where(StudentDB.email == student.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="El correo ya está registrado")
    db_student = StudentDB(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return StudentResponse(message="Estudiante creado exitosamente", student=db_student)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentBase, db: Session = Depends(get_db)):
    db_student = db.get(StudentDB, student_id)
    if not db_student or not db_student.is_active:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    email_exists = db.execute(
        select(StudentDB).where(StudentDB.email == student.email, StudentDB.id != student_id)
    ).scalar_one_or_none()
    if email_exists:
        raise HTTPException(status_code=409, detail="El correo ya está en uso")

    for key, value in student.dict().items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return StudentResponse(message="Estudiante actualizado exitosamente", student=db_student)

@router.delete("/{student_id}", response_model=StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.get(StudentDB, student_id)
    if not db_student or not db_student.is_active:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    db_student.is_active = False
    db.commit()
    return StudentResponse(message="Estudiante eliminado exitosamente", student=db_student)
