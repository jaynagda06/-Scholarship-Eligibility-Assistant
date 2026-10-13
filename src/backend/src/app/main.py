import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from app import services
from app.config import settings as app_settings
from app import services as app_services
from app.main import app as backend_app

app = FastAPI(
    title="Scholarship Eligibility Assistant",
    description="AI-driven scholarship eligibility and recommendation platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[s.strip() for s in app_settings.CORS_ORIGINS.split(',')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return backend_app.health()


@app.get("/scholarships")
def list_scholarships(limit: int = 50, category: str = None, status: str = None):
    return backend_app.list_scholarships(limit=limit, category=category, status=status)


@app.get("/scholarships/{scholarship_id}")
def get_scholarship(scholarship_id: int):
    return backend_app.get_scholarship(scholarship_id)


@app.post("/scholarships")
def create_scholarship(data: dict):
    return backend_app.create_scholarship(data)


@app.get("/students")
def list_students(limit: int = 50, q: str = None):
    return backend_app.list_students(limit=limit, q=q)


@app.get("/students/{student_id}")
def get_student(student_id: int):
    return backend_app.get_student(student_id)


@app.post("/students")
def create_student(data: dict):
    return backend_app.create_student(data)


@app.post("/students/{student_id}/eligibility")
def eligibility_check(student_id: int, limit: int = 10):
    return backend_app.eligibility_check(student_id=student_id, limit=limit)
