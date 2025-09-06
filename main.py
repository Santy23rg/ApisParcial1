from fastapi import FastAPI
from routers import students, teachers, subjects, notes

app = FastAPI(title="Parcial 1 API")

app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(subjects.router)
app.include_router(notes.router)
