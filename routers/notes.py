from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from database.connection import SessionLocal
from models.schemas import NoteDB, NoteBase, NoteResponse, Note, SubjectDB

router = APIRouter(prefix="/notes", tags=["Notas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Note])
def get_notes(db: Session = Depends(get_db)):
    stmt = select(NoteDB).where(NoteDB.is_active == True)
    return db.execute(stmt).scalars().all()

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteBase, db: Session = Depends(get_db)):
    db_note = NoteDB(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return NoteResponse(message="Nota creada exitosamente", note=db_note)

@router.get("/promedio/")
def get_student_average(
    student_id: int = Query(..., description="ID del estudiante"),
    subject_id: int = Query(..., description="ID de la materia"),
    db: Session = Depends(get_db)
):
    stmt = select(func.avg(NoteDB.grade)).where(
        NoteDB.student_id == student_id,
        NoteDB.subject_id == subject_id,
        NoteDB.is_active == True
    )
    avg = db.execute(stmt).scalar()
    if avg is None:
        raise HTTPException(status_code=404, detail="No hay notas para este estudiante en la materia seleccionada")
    return {"mensaje": "Promedio calculado exitosamente", "promedio": round(avg, 2)}
