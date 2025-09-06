from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.connection import SessionLocal
from models.schemas import TeacherDB, TeacherBase, TeacherResponse, Teacher

router = APIRouter(prefix="/teachers", tags=["Profesores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Teacher])
def get_teachers(db: Session = Depends(get_db)):
    stmt = select(TeacherDB).where(TeacherDB.is_active == True)
    return db.execute(stmt).scalars().all()

@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher: TeacherBase, db: Session = Depends(get_db)):
    db_teacher = TeacherDB(**teacher.dict())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return TeacherResponse(message="Profesor creado exitosamente", teacher=db_teacher)

@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(teacher_id: int, teacher: TeacherBase, db: Session = Depends(get_db)):
    db_teacher = db.get(TeacherDB, teacher_id)
    if not db_teacher or not db_teacher.is_active:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    for key, value in teacher.dict().items():
        setattr(db_teacher, key, value)

    db.commit()
    db.refresh(db_teacher)
    return TeacherResponse(message="Profesor actualizado exitosamente", teacher=db_teacher)

@router.delete("/{teacher_id}", response_model=TeacherResponse)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = db.get(TeacherDB, teacher_id)
    if not db_teacher or not db_teacher.is_active:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    db_teacher.is_active = False
    db.commit()
    return TeacherResponse(message="Profesor eliminado exitosamente", teacher=db_teacher)
