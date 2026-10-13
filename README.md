# Scholarship Eligibility Assistant

AI-driven scholarship recommendation platform

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+

### Run Everything
Double click `run_all.bat` or run:
```bash
cd D:\Projects\Scholarship
run_all.bat
```

### Manual Start
Backend:
```bash
cd src\backend
pip install -r pyproject.toml  # or install fastapi uvicorn
python run_server.py
```

Frontend:
```bash
cd src\frontend
npm install vite
npm run dev
```

## API Endpoints
- GET /health - Health check
- GET /scholarships - List scholarships
- GET /scholarships/{id} - Get scholarship details
- POST /scholarships - Create scholarship (admin)
- GET /students - List students
- POST /students - Create student
- POST /students/{id}/eligibility - Check scholarship eligibility

## Project Structure
```
src/
  backend/      # FastAPI backend
  frontend/     # React frontend
docs/          # Documentation
scripts/       # Seed and deploy scripts
infra/         # Infrastructure
tests/         # Tests
```
