from core.logger import app_logger
from rag.chunker import text_chunker
from rag.embeddings import embedding_service
from rag.pdf_loader import pdf_loader
from rag.retriever import retriever
from rag.vector_store import vector_store


class RAGPipeline:
    def ingest_pdf(self, file_path: str) -> int:
        app_logger.info(
            f"Starting PDF ingestion: {file_path}"
        )

        content = pdf_loader.load(file_path)

        chunks = text_chunker.split(content)

        if not chunks:
            raise ValueError(
                "No text chunks generated from PDF"
            )

        embeddings = embedding_service.embed_documents(
            chunks
        )

        vector_store.add(
            documents=chunks,
            embeddings=embeddings,
        )

        app_logger.success(
            f"PDF ingestion completed: {len(chunks)} chunks"
        )

        return len(chunks)

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict]:
        return retriever.retrieve(
            query=query,
            top_k=top_k,
        )


rag_pipeline = RAGPipeline()