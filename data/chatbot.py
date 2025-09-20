import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_FILE = "msu_index.faiss"
META_FILE = "msu_index.pkl"


print("🔄 Loading model and index...")
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(INDEX_FILE)
with open(META_FILE, "rb") as f:
    chunks = pickle.load(f)
print("✅ Ready! Ask me about MSU Main.\n")


def search(query, k=3):
    xq = model.encode([query])
    D, I = index.search(np.array(xq).astype("float32"), k)
    print("\n[DEBUG] Raw FAISS results:", I[0], D[0])  # 👈
    results = []
    for rank, idx in enumerate(I[0]):
        idx = int(idx)
        if 0 <= idx < len(chunks):
            results.append((chunks[idx], float(D[0][rank])))
    return results



def main():
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            break
        results = search(query, k=3)

        if not results:
            print("🤖 MSU AI: Sorry, I couldn’t find anything about that in my MSU knowledge.\n")
        else:
            print("\n🤖 MSU AI: Based on my knowledge...\n")
            for i, (chunk, score) in enumerate(results, start=1):
                print(f"{i}. {chunk[:300]}...\n") 


if __name__ == "__main__":
    main()
