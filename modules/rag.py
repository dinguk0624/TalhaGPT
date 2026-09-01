# modules/rag.py

import os
import uuid

import chromadb
from sentence_transformers import SentenceTransformer


print("[RAG] Loading embedding model...")


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedder = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ============================================================
# VECTOR DATABASE
# ============================================================

db_client = chromadb.PersistentClient(
    path="./vector_db"
)

collection = db_client.get_or_create_collection(
    name="talha_knowledge"
)


# ============================================================
# TEXT CHUNKING
# ============================================================

def _split_text(
    text: str,
    chunk_size: int = 500
) -> list[str]:
    """
    Split text into manageable chunks.
    """

    if not text or not text.strip():
        return []

    if chunk_size <= 0:
        chunk_size = 500

    raw_chunks = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []

    for paragraph in raw_chunks:

        if len(paragraph) <= chunk_size:

            chunks.append(
                paragraph
            )

        else:

            for i in range(
                0,
                len(paragraph),
                chunk_size
            ):

                chunk = paragraph[
                    i:i + chunk_size
                ].strip()

                if chunk:
                    chunks.append(
                        chunk
                    )

    return chunks


# ============================================================
# ADD TEXT TO MEMORY
# ============================================================

def add_text_to_memory(
    text: str,
    source: str = "user_note"
) -> str:
    """
    Add plain text to TalhaGPT's long-term RAG memory.
    """

    if not text or not text.strip():

        return (
            "[RAG Error]: "
            "Cannot add empty text to memory."
        )

    text = text.strip()

    chunks = _split_text(
        text
    )

    if not chunks:

        return (
            "[RAG Error]: "
            "No valid text chunks were created."
        )

    ids = [
        f"memory_{uuid.uuid4().hex}"
        for _ in chunks
    ]

    # --------------------------------------------------------
    # GENERATE EMBEDDINGS
    # --------------------------------------------------------

    try:

        embeddings = embedder.encode(
            chunks
        ).tolist()

    except Exception as e:

        return (
            "[RAG Error]: "
            f"Failed to generate embeddings: {e}"
        )

    # --------------------------------------------------------
    # STORE MEMORY
    # --------------------------------------------------------

    try:

        collection.upsert(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=[
                {
                    "source": source,
                    "type": "long_term_memory"
                }
                for _ in chunks
            ]
        )

    except Exception as e:

        return (
            "[RAG Error]: "
            f"Failed to store memory: {e}"
        )

    return (
        "[RAG]: "
        "Text successfully added to long-term memory. "
        f"({len(chunks)} chunks)"
    )


# ============================================================
# ADD DOCUMENT TO MEMORY
# ============================================================

def add_document_to_memory(
    file_path: str
) -> str:
    """
    Read a text document and add it to long-term RAG memory.
    """

    if not file_path or not file_path.strip():

        return (
            "[RAG Error]: "
            "File path cannot be empty."
        )

    clean_path = (
        file_path
        .strip()
        .strip("'\"")
    )

    # --------------------------------------------------------
    # NORMALIZE ROOT-STYLE PATH
    # --------------------------------------------------------

    if clean_path.startswith("/"):

        clean_path = clean_path.lstrip(
            "/\\"
        )

    # --------------------------------------------------------
    # PROJECT ROOT
    # --------------------------------------------------------

    project_root = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )

    # --------------------------------------------------------
    # RESOLVE RELATIVE PATH
    # --------------------------------------------------------

    if not os.path.isabs(
        clean_path
    ):

        clean_path = os.path.join(
            project_root,
            clean_path
        )

    clean_path = os.path.normpath(
        clean_path
    )

    # --------------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------------

    if not os.path.isfile(
        clean_path
    ):

        return (
            "[RAG Error]: "
            f"File '{clean_path}' was not found."
        )

    # --------------------------------------------------------
    # READ FILE
    # --------------------------------------------------------

    try:

        with open(
            clean_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

    except Exception as e:

        return (
            "[RAG Error]: "
            f"Failed to read file: {e}"
        )

    # --------------------------------------------------------
    # SPLIT DOCUMENT
    # --------------------------------------------------------

    chunks = _split_text(
        content
    )

    if not chunks:

        return (
            "[RAG]: "
            "The file is empty."
        )

    file_name = os.path.basename(
        clean_path
    )

    ids = [
        f"document_{uuid.uuid4().hex}"
        for _ in chunks
    ]

    # --------------------------------------------------------
    # GENERATE EMBEDDINGS
    # --------------------------------------------------------

    try:

        embeddings = embedder.encode(
            chunks
        ).tolist()

    except Exception as e:

        return (
            "[RAG Error]: "
            f"Failed to generate embeddings: {e}"
        )

    # --------------------------------------------------------
    # STORE DOCUMENT
    # --------------------------------------------------------

    try:

        collection.upsert(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=[
                {
                    "source": clean_path,
                    "type": "document",
                    "file_name": file_name
                }
                for _ in chunks
            ]
        )

    except Exception as e:

        return (
            "[RAG Error]: "
            f"Failed to store document: {e}"
        )

    return (
        "[RAG]: "
        f"'{file_name}' was successfully "
        "indexed into memory. "
        f"({len(chunks)} chunks)"
    )


# ============================================================
# SEARCH MEMORY
# ============================================================

def search_memory(
    query: str,
    n_results: int = 2
) -> str:
    """
    Search long-term RAG memory for relevant information.
    """

    if not query or not query.strip():
        return ""

    if n_results <= 0:
        n_results = 2

    try:

        query_embedding = embedder.encode(
            [query]
        ).tolist()

        results = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        if not documents:
            return ""

        return "\n---\n".join(
            documents
        )

    except Exception as e:

        print(
            f"[RAG Search Error]: {e}"
        )

        return ""
