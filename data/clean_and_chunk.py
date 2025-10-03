import re
from pathlib import Path

RAW_FILE = "msu_textbook.txt"
CLEAN_FILE = "msu_cleaned.txt"
CHUNKS_FILE = "msu_chunks.txt"

def clean_text(text):
  
    text = re.sub(r"\n\s*\n", "\n", text)  
    text = re.sub(r"\s{2,}", " ", text)    
    text = re.sub(r"\n\d+\n", "\n", text)  
    return text.strip()

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into chunks with overlap.
    chunk_size = characters per chunk
    overlap = how much each chunk overlaps with the previous one
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap  
    return chunks

def main():
    p = Path(RAW_FILE)
    if not p.exists():
        print(f"File {RAW_FILE} not found. Run Step 1 first.")
        return
    
    text = p.read_text(encoding="utf-8")
    cleaned = clean_text(text)
    Path(CLEAN_FILE).write_text(cleaned, encoding="utf-8")
    print(f"Cleaned text saved to {CLEAN_FILE}, length = {len(cleaned)} characters")

    chunks = chunk_text(cleaned, chunk_size=500, overlap=50)
    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks, start=1):
            f.write(f"### Chunk {i}\n{chunk}\n\n")
    print(f"Created {len(chunks)} chunks, saved to {CHUNKS_FILE}")

    print("\n--- SAMPLE CHUNK ---\n")
    print(chunks[0][:400])  
    print("\n--- END SAMPLE ---\n")

if __name__ == "__main__":
    main()
