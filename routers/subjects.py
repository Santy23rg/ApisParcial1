from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.connection import SessionLocal
from models.schemas import SubjectDB, SubjectBase, SubjectResponse, Subject

router = APIRouter(prefix="/subjects", tags=["Materias"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Subject])
def get_subjects(db: Session = Depends(get_db)):
    stmt = select(SubjectDB).where(SubjectDB.is_active == True)
    return db.execute(stmt).scalars().all()

@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(subject: SubjectBase, db: Session = Depends(get_db)):
    db_subject = SubjectDB(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return SubjectResponse(message="Materia creada exitosamente", subject=db_subject)

@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(subject_id: int, subject: SubjectBase, db: Session = Depends(get_db)):
    db_subject = db.get(SubjectDB, subject_id)
    if not db_subject or not db_subject.is_active:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    for key, value in subject.dict().items():
        setattr(db_subject, key, value)

    db.commit()
    db.refresh(db_subject)
    return SubjectResponse(message="Materia actualizada exitosamente", subject=db_subject)

@router.delete("/{subject_id}", response_model=SubjectResponse)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = db.get(SubjectDB, subject_id)
    if not db_subject or not db_subject.is_active:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    db_subject.is_active = False
    db.commit()
    return SubjectResponse(message="Materia eliminada exitosamente", subject=db_subject)
