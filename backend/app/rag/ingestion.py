import uuid
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.knowledge_document import KnowledgeDocument
from app.rag.document_loader import load_pdf
from app.rag.embeddings import generate_embeddings
from app.rag.text_chunker import chunk_text
from app.rag.vector_store import add_documents


def ingest_knowledge_document(
    file_path: str,
    document_name: str,
    document_type: str,
    version: str,
    source: str,
    description: str | None,
    effective_date: datetime | None,
    db: Session,
) -> dict:

    path = Path(file_path)

    if not path.exists():
        raise ValueError(
            f"Knowledge document not found: {file_path}"
        )

    text = load_pdf(str(path))

    if not text.strip():
        raise ValueError(
            "Knowledge document contains no extractable text."
        )

    chunks = chunk_text(text)

    if not chunks:
        raise ValueError(
            "No chunks were generated from the document."
        )

    embeddings = generate_embeddings(
        [chunk.text for chunk in chunks]
    )

    document_id = uuid.uuid4()

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        chunk_id = (
            f"{document_id}:"
            f"{chunk.chunk_index}"
        )

        ids.append(chunk_id)

        documents.append(chunk.text)

        metadatas.append(
            {
                "knowledge_document_id": str(
                    document_id
                ),
                "document_name": document_name,
                "document_type": document_type,
                "version": version,
                "source": source,
                "chunk_index": chunk.chunk_index,
                "effective_date": (
                    effective_date.isoformat()
                    if effective_date
                    else ""
                ),
            }
        )

    add_documents(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    knowledge_document = KnowledgeDocument(
        id=document_id,
        document_name=document_name,
        document_type=document_type,
        version=version,
        effective_date=effective_date,
        source=source,
        description=description,
        file_path=str(path),
        active=True,
        chunk_count=len(chunks),
    )

    db.add(knowledge_document)
    db.commit()
    db.refresh(knowledge_document)

    return {
        "document": knowledge_document,
        "chunk_count": len(chunks),
    }