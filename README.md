# Scholarship Eligibility Assistant

AI-driven scholarship recommendation platform. Students register a profile, the
matching engine scores every scholarship against that profile, and the dashboard
shows ranked recommendations.

## Stack

| Part     | Technology                                              |
| -------- | ------------------------------------------------------- |
| Frontend | Single-file React 18 (UMD) + Babel, built with Vite     |
| Backend  | FastAPI + SQLite                                        |
| Hosting  | Vercel (Services: Vite frontend + FastAPI backend)      |

## Local development

### Prerequisites
- Python 3.12+ (3.13 recommended)
- Node.js 20+

### One command

```bat
run_all.bat
```

### Manual

Backend (terminal 1):

```bash
cd src/backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 3000
```

Frontend (terminal 2):

```bash
cd src/frontend
npm install
npm run dev
```

Open http://localhost:5173. The Vite dev server proxies `/api/*` to
`http://127.0.0.1:3000`, so the frontend always calls a relative `/api` base.

## API

All routes are served under `/api`.

| Method | Path                             | Description                        |
| ------ | -------------------------------- | ---------------------------------- |
| GET    | `/api/health`                    | Health check                       |
| GET    | `/api/scholarships`              | List scholarships                  |
| GET    | `/api/scholarships/{id}`         | Get one scholarship                |
| POST   | `/api/scholarships`              | Create a scholarship               |
| GET    | `/api/students`                  | List students                      |
| GET    | `/api/students/{id}`             | Get one student                    |
| POST   | `/api/students`                  | Create a student                   |
| POST   | `/api/students/{id}/eligibility` | Score scholarships for the student |
| POST   | `/api/seed`                      | Re-seed demo data                  |

Interactive docs: http://localhost:3000/docs

## Deploying to Vercel

The repository is pre-configured with `vercel.json`, which declares two
[Vercel Services](https://vercel.com/docs/services):

- `frontend` → `src/frontend/` (Vite)
- `backend` → `src/backend/` (FastAPI, entrypoint `app.main:app`)

Requests to `/api/*` go to the backend; everything else goes to the frontend.

### Import the repository

1. Go to <https://vercel.com/new> and import this GitHub repository.
2. Leave **Root Directory** as `./` — `vercel.json` handles the rest.
3. Framework Preset: **Other** (do not override it; the services define their own).
4. Build & Output settings: leave empty.
5. No environment variables are required.
6. Click **Deploy**.

### Notes

- On Vercel the SQLite database lives in `/tmp` (the only writable path) and is
  recreated and seeded automatically on cold start. Data is therefore
  per-instance and resets when a function instance is recycled — fine for a
  demo, not for production persistence.
- Python version is pinned by `src/backend/.python-version` and
  `src/backend/pyproject.toml`.

## Project structure

```
src/
  backend/          # FastAPI app
    app/
      main.py       # routes (mounted under /api)
      services/     # database, students, scholarships, matching
      config/       # pydantic settings
  frontend/
    index.html      # entire UI (React UMD + Babel)
docs/               # architecture notes
vercel.json         # Vercel Services config
```
