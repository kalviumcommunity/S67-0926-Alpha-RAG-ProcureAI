from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.routes.documents import router as documents_router
from app.api.routes.chat import router as chat_router
from app.api.routes.suppliers import router as suppliers_router
from app.db.database import get_db


app = FastAPI(
    title="Procurement Document Intelligence API",
    version="0.1.0",
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.get("/api/health/db")
def database_health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


app.include_router(
    documents_router,
    prefix="/api",
)

app.include_router(
    suppliers_router,
    prefix="/api",
)

app.include_router(
    chat_router,
    prefix="/api",
)