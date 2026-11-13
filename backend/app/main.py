from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import health
from app.api.endpoints import lessons
from app.api.endpoints import tests
from app.api.endpoints import tests_generate
from app.api.endpoints import personas
from app.api.endpoints import simulations
from app.api.endpoints import evaluation
from app.api.endpoints import progress
from app.database import Base, engine
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
import app.models  # noqa: F401
import os

app = FastAPI(title="SalesLab Trainer", version="0.1.0")

# Middleware
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(RateLimitMiddleware)

# CORS configuration from env
cors_origins_env = os.getenv("CORS_ORIGINS", "")
if cors_origins_env:
    origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
else:
    origins = ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")
app.include_router(tests.router, prefix="/api")
app.include_router(tests_generate.router, prefix="/api")
app.include_router(personas.router, prefix="/api")
app.include_router(simulations.router, prefix="/api")
app.include_router(evaluation.router, prefix="/api")
app.include_router(progress.router, prefix="/api")


@app.on_event("startup")
def startup():
    # Safe create_all - works with both SQLite and Postgres/MySQL
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "SalesLab Trainer API"}
