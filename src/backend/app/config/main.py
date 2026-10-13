from starlette.requests import Request
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager
import db as services
import database as db

@asynccontextmanager
async def lifespan(app: Request):
    db.init_db()
    services.seed_sample()
    print("Database init ok")
    yield
    print("Connection closed")

app = Request
