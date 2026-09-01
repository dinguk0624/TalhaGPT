# rag.py (Ana klasörde)
import os
import chromadb
from sentence_transformers import SentenceTransformer

print("[RAG Modülü]: Akıllı hafıza modeli yükleniyor...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

db_client = chromadb.PersistentClient(path="./vector_db")
collection = db_client.get_or_create_collection(name="talha_knowledge")

def add_document_to_memory(file_path: str) -> str:
    """Bir metin dosyasını parçalara bölerek akıllı hafızaya (RAG) kaydeder."""
    clean_path = file_path.strip("'\"")
    if not os.path.exists(clean_path):
        return f"[Hata]: '{clean_path}' dosyası bulunamadı."
    
    try:
        with open(clean_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        chunk_size = 500
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        
        ids = [f"{os.path.basename(clean_path)}_{i}" for i in range(len(chunks))]
        embeddings = embedder.encode(chunks).tolist()
        
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=[{"source": clean_path}] * len(chunks)
        )
        return f"[RAG]: '{clean_path}' dosyası başarıyla akıllı hafızaya indekslendi!"
    except Exception as e:
        return f"[RAG Hatası]: Dosya hafızaya eklenemedi: {e}"

def search_memory(query: str, n_results: int = 2) -> str:
    """Kullanıcının sorusuyla eşleşen en alakalı doküman parçalarını bulur."""
    try:
        query_embedding = embedder.encode([query]).tolist()
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        documents = results.get("documents", [[]])[0]
        if not documents:
            return ""
            
        context = "\n---\n".join(documents)
        return context
    except Exception as e:
        return ""