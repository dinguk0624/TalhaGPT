import hashlib
import os

from modules.file_reader import _resolve_safe_path


_embedder = None
_collection = None


def _get_embedder():
    """Load the embedding model only when RAG functionality is first used."""
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer

        print("[RAG] Loading embedding model...")
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder


def _get_collection():
    """Open ChromaDB only when RAG is actually used."""
    global _collection
    if _collection is None:
        import chromadb

        db_client = chromadb.PersistentClient(path="./vector_db")
        _collection = db_client.get_or_create_collection(name="talha_knowledge")
    return _collection


def _split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Simple paragraph + fixed-size chunking with optional overlap."""
    if not text or not text.strip():
        return []
    if chunk_size <= 0:
        chunk_size = 500
    if overlap < 0:
        overlap = 0
    if overlap >= chunk_size:
        overlap = chunk_size // 5

    raw_chunks = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    for paragraph in raw_chunks:
        if len(paragraph) <= chunk_size:
            chunks.append(paragraph)
        else:
            step = chunk_size - overlap
            for i in range(0, len(paragraph), step):
                piece = paragraph[i : i + chunk_size].strip()
                if piece:
                    chunks.append(piece)
    return chunks


def _content_id(prefix: str, content: str) -> str:
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return f"{prefix}_{digest}"


def _store_chunks(
    chunks: list[str],
    source: str,
    memory_type: str,
    prefix: str,
    file_name: str | None = None,
) -> str:
    if not chunks:
        return "[RAG]: No valid text chunks were created."
    ids = [_content_id(prefix, chunk) for chunk in chunks]
    try:
        embeddings = _get_embedder().encode(chunks).tolist()
        metadatas = [
            {"source": source, "type": memory_type, **({"file_name": file_name} if file_name else {})}
            for _ in chunks
        ]
        _get_collection().upsert(
            documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas
        )
    except Exception as exc:
        return f"[RAG Error]: Failed to store memory: {type(exc).__name__}"
    return f"[RAG]: Text successfully added to long-term memory. ({len(chunks)} chunks)"


def add_text_to_memory(text: str, source: str = "user_note") -> str:
    if not text or not text.strip():
        return "[RAG Error]: Cannot add empty text to memory."
    return _store_chunks(_split_text(text.strip()), source, "long_term_memory", "memory")


def add_document_to_memory(file_path: str) -> str:
    path, err = _resolve_safe_path(file_path)
    if err:
        return f"[RAG Error]: {err}"
    clean_path = str(path)

    try:
        with open(clean_path, "r", encoding="utf-8") as file:
            content = file.read()
    except (OSError, UnicodeError):
        return "[RAG Error]: Failed to read the requested file."

    chunks = _split_text(content)
    if not chunks:
        return "[RAG]: The file is empty."

    file_name = os.path.basename(clean_path)
    return _store_chunks(chunks, clean_path, "document", "document", file_name)


def search_memory(query: str, n_results: int = 4) -> str:
    if not query or not query.strip():
        return "[Memory]: Search query was empty. Do not invent remembered information."
    if isinstance(n_results, bool) or not isinstance(n_results, int):
        n_results = 4
    n_results = max(1, min(n_results, 10))

    try:
        query_embedding = _get_embedder().encode([query]).tolist()
        results = _get_collection().query(
            query_embeddings=query_embedding, n_results=n_results
        )
        documents = results.get("documents", [[]])[0]
        if documents:
            return "\n---\n".join(documents)
        return "[Memory]: No relevant notes were found. Do not invent remembered information."
    except Exception as exc:
        print(f"[RAG Search Error]: {type(exc).__name__}")
        return (
            "[Memory]: Search failed. Do not invent remembered information."
        )
