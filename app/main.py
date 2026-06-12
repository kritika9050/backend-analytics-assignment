from fastapi import FastAPI
from app.database import Base, engine
from app.mock_api import router as mock_router
from app.ingestion import router as ingestion_router
from app.analytics import router as analytics_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Large Data Analytics Backend",
    description="FastAPI backend for mock API ingestion, PostgreSQL storage, and sub-2-second analytics.",
    version="1.0.0",
)

app.include_router(mock_router)
app.include_router(ingestion_router)
app.include_router(analytics_router)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Large Data Analytics Backend is running"}
