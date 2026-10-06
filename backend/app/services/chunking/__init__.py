from typing import Iterable, List, Optional, TypedDict

from app.core.config import settings
from app.db.models import DocumentContent


class DocumentChunk(TypedDict):
	document_id: int
	document_name: str
	page_number: int
	section: Optional[str]
	chunk_id: str
	content: str


def chunk_document_content(
	document_content: DocumentContent,
) -> List[DocumentChunk]:
	content = document_content.content
	if not content or not content.strip():
		return []

	if document_content.document is None:
		raise ValueError(
			"DocumentContent must be associated with a Document to create chunks"
		)

	document_name = document_content.document.filename
	step = settings.chunk_size - settings.chunk_overlap
	chunks: List[DocumentChunk] = []
	start = 0
	chunk_index = 1

	while start < len(content):
		end = min(start + settings.chunk_size, len(content))
		chunks.append(
			{
				"document_id": document_content.document_id,
				"document_name": document_name,
				"page_number": document_content.page_number,
				"section": document_content.section,
				"chunk_id": (
					f"doc-{document_content.document_id}-"
					f"page-{document_content.page_number}-chunk-{chunk_index}"
				),
				"content": content[start:end],
			}
		)
		if end == len(content):
			break
		start += step
		chunk_index += 1

	return chunks


def chunk_document_contents(
	document_contents: Iterable[DocumentContent],
) -> List[DocumentChunk]:
	chunks: List[DocumentChunk] = []
	for document_content in document_contents:
		chunks.extend(chunk_document_content(document_content))
	return chunks


__all__ = [
	"DocumentChunk",
	"chunk_document_content",
	"chunk_document_contents",
]
