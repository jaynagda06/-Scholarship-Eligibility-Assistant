from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from . import services

app = FastAPI(
    title="Scholarship Eligibility Assistant",
    description="AI-driven scholarship eligibility and recommendation platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/scholarships")
def list_scholarships(limit: int = 50, category: str = None, status: str = None):
    categories = [category] if category else None
    statuses = [status] if status else None
    return services.scholarship_service.list_scholarships(limit=limit, categories=categories, status=statuses)


@app.get("/scholarships/{scholarship_id}")
def get_scholarship(scholarship_id: int):
    s = services.scholarship_service.get_scholarship(scholarship_id)
    if not s:
        return {"error": "not found"}, 404
    return s


@app.post("/scholarships")
def create_scholarship(data: dict):
    sid = services.scholarship_service.create_scholarship(data)
    return {"id": sid, "status": "created"}


@app.get("/students")
def list_students(limit: int = 50, q: str = None):
    return services.student_service.list_students(limit=limit, phone=q)


@app.get("/students/{student_id}")
def get_student(student_id: int):
    s = services.student_service.get_student(student_id)
    if not s:
        return {"error": "not found"}, 404
    return s


@app.post("/students")
def create_student(data: dict):
    st = services.student_service.create_student(data)
    return {"id": st, "status": "created"}


@app.post("/students/{student_id}/eligibility")
def eligibility_check(student_id: int, limit: int = 10):
    return services.matching_service.check_eligibility(student_id, limit)


@app.post("/seed")
def seed_data():
    services.database.init_db()
    services.scholarship_service.seed_sample()
    services.student_service.seed_sample()
    return {"status": "seeded"}
