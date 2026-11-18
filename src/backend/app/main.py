from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import services
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise the database and seed demo data on cold start.

    On Vercel the filesystem is read-only except for /tmp, so the database
    lives there and is recreated automatically whenever a function boots.
    """
    services.database.init_db()
    services.scholarship_service.seed_if_empty()
    services.student_service.seed_if_empty()
    yield


app = FastAPI(
    title="Scholarship Eligibility Assistant",
    description="AI-driven scholarship eligibility and recommendation platform",
    version="0.1.0",
    lifespan=lifespan,
)

# The frontend and API share a domain on Vercel (Services routing), so CORS is
# only needed for local development where Vite proxies /api to this server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter(prefix="/api")


@api.get("/health")
def health():
    return {"status": "ok"}


@api.get("/scholarships")
def list_scholarships(limit: int = 50, category: str = None, status: str = None):
    categories = [category] if category else None
    statuses = [status] if status else None
    return services.scholarship_service.list_scholarships(
        limit=limit, categories=categories, status=statuses
    )


@api.get("/scholarships/{scholarship_id}")
def get_scholarship(scholarship_id: int):
    scholarship = services.scholarship_service.get_scholarship(scholarship_id)
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return scholarship


@api.post("/scholarships")
def create_scholarship(data: dict):
    scholarship_id = services.scholarship_service.create_scholarship(data)
    return {"id": scholarship_id, "status": "created"}


@api.get("/students")
def list_students(limit: int = 50, q: str = None):
    return services.student_service.list_students(limit=limit, phone=q)


@api.get("/students/{student_id}")
def get_student(student_id: int):
    student = services.student_service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@api.post("/students")
def create_student(data: dict):
    student_id = services.student_service.create_student(data)
    return {"id": student_id, "status": "created"}


@api.post("/students/{student_id}/eligibility")
def eligibility_check(student_id: int, limit: int = 10):
    result = services.matching_service.check_eligibility(student_id, limit)
    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@api.post("/seed")
def seed_data():
    services.database.init_db()
    services.scholarship_service.seed_sample()
    services.student_service.seed_sample()
    return {"status": "seeded"}


app.include_router(api)


@app.get("/health")
def root_health():
    """Kept for simple uptime checks and backwards compatibility."""
    return {"status": "ok"}
