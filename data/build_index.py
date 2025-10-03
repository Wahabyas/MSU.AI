import faiss
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "msu_chunks.txt"
INDEX_FILE = "msu_index.faiss"
META_FILE = "msu_index.pkl"

def load_chunks():
    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        content = f.read().split("### Chunk ")
        for c in content:
            if c.strip():
                parts = c.split("\n", 1)
                if len(parts) > 1:
                    chunks.append(parts[1].strip())
    return chunks

def main():
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks")


    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks, show_progress_bar=True)


    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)


    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "wb") as f:
        pickle.dump({"chunks": chunks}, f)

    print(f"Saved index to {INDEX_FILE} and metadata to {META_FILE}")

if __name__ == "__main__":
    main()
