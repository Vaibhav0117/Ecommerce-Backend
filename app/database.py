from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# 1. Database URL
# For SQLite (local file-based DB)
SQLALCHEMY_DATABASE_URL = "sqlite:///./food_app.db"

# 2. Engine
# The engine is the core connection to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. SessionLocal
# Session is how we talk to the DB (like opening a cursor)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base
# Base class for all models (tables will inherit from this)
Base = declarative_base()

# Dependency function for FastAPI routes
# Opens a new database session for each request,
# yields it to the route handler, and ensures the session
# is closed after the request is finished.
# This prevents connection leaks and keeps transactions safe.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
