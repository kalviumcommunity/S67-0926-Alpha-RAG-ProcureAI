import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

DEFAULT_UPLOAD_DIRECTORY = Path(__file__).resolve().parents[2] / "uploads"


class Settings(BaseModel):
    app_name: str = "Procurement Document Intelligence API"
    app_version: str = "0.1.0"
    database_url: str = os.getenv("DATABASE_URL", "")
    max_upload_size_mb: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))
    upload_directory: Path = Path(
        os.getenv("UPLOAD_DIRECTORY", str(DEFAULT_UPLOAD_DIRECTORY))
    )
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    )
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "./vector_db")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "local-model")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024


settings = Settings()

if settings.chunk_size <= 0:
    raise ValueError("CHUNK_SIZE must be greater than zero")
if settings.chunk_overlap < 0 or settings.chunk_overlap >= settings.chunk_size:
    raise ValueError("CHUNK_OVERLAP must be non-negative and less than CHUNK_SIZE")