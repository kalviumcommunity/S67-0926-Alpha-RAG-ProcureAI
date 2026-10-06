from pathlib import Path
from typing import Final, List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status as http_status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.services.retrieval import delete_document_chunks
from app.core.config import settings
from app.db.database import get_db
from app.db.models import Document, DocumentStatus, DocumentType, Supplier
from app.schemas import DocumentMetadataResponse, DocumentResponse
from app.services.ai_service import process_document
from app.storage.files import (
    FileSizeLimitExceeded,
    delete_stored_file,
    save_upload_file,
    stored_file_from_reference,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


SUPPORTED_FILE_TYPES: Final = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
}


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=http_status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    supplier_id: int = Form(...),
    document_type: str = Form(...),
    db: Session = Depends(get_db),
):
    original_filename = file.filename or ""
    extension = Path(original_filename).suffix.lower()
    expected_mime_type = SUPPORTED_FILE_TYPES.get(extension)
    if expected_mime_type is None or file.content_type != expected_mime_type:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file extension or MIME type",
        )

    try:
        parsed_document_type = DocumentType(document_type)
    except ValueError:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="Invalid document_type",
        )

    supplier = db.get(Supplier, supplier_id)
    if supplier is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Supplier {supplier_id} not found",
        )

    try:
        stored_file = await save_upload_file(
            upload_file=file,
            extension=extension,
            upload_directory=settings.upload_directory,
            max_size_bytes=settings.max_upload_size_bytes,
        )
    except FileSizeLimitExceeded:
        raise HTTPException(
            status_code=http_status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Uploaded file exceeds the configured size limit",
        )
    except OSError:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to store uploaded file",
        )

    try:
        document = Document(
            supplier_id=supplier_id,
            filename=original_filename,
            document_type=parsed_document_type,
            file_path=stored_file.relative_path,
            file_size=stored_file.file_size,
            mime_type=expected_mime_type,
            status=DocumentStatus.UPLOADED,
        )
        db.add(document)
        db.commit()
        db.refresh(document)
    except Exception:
        db.rollback()
        await delete_stored_file(stored_file, missing_ok=True)
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create document record",
        )

    try:
        process_document(document.id)
    except HTTPException:
        db.refresh(document)
        raise

    db.refresh(document)
    return document


@router.post("/{document_id}/process", response_model=DocumentResponse)
def process_document_endpoint(
    document_id: int,
    db: Session = Depends(get_db),
):
    process_document(document_id)
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found",
        )
    return document


@router.get("", response_model=List[DocumentResponse])
def list_documents(
    supplier_id: Optional[int] = Query(default=None),
    document_type: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    statement = select(Document).order_by(Document.id)

    if supplier_id is not None:
        statement = statement.where(Document.supplier_id == supplier_id)
    if document_type is not None:
        try:
            parsed_document_type = DocumentType(document_type)
        except ValueError:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Invalid document_type filter",
            )
        statement = statement.where(Document.document_type == parsed_document_type)
    if status is not None:
        try:
            parsed_status = DocumentStatus(status)
        except ValueError:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Invalid status filter",
            )
        statement = statement.where(Document.status == parsed_status)

    return db.scalars(statement).all()


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found",
        )
    return document


@router.get("/{document_id}/metadata", response_model=DocumentMetadataResponse)
def get_document_metadata(document_id: int, db: Session = Depends(get_db)):
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found",
        )
    if document.metadata_record is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Metadata for document {document_id} not found",
        )
    return document.metadata_record


@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found",
        )

    stored_file = stored_file_from_reference(
        document.file_path,
        settings.upload_directory,
    )
    try:
        await delete_stored_file(stored_file)
    except OSError:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete stored document file",
        )

    delete_document_chunks(document_id)

    try:
        db.delete(document)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete document record",
        )

    return {"message": "Document deleted successfully"}