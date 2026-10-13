import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings
from . import database as db
from . import services

# Lazy-load on first request
db.init_db = db.init_db
