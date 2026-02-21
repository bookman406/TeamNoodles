import json, os, re
from typing import List
import requests
import faiss
import numpy as np

OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"

def chunk(text: str, size: int = 900, overlap: int = 150) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    out, i = [], 0
    while i < len(text):
        j = min(len(text), i + size)
        out.append(text[i:j])
        if j == len(text):
            break
        i = max(0, j - overlap)
    return out

def embed_texts(texts: List[str]) -> np.ndarray:
    vectors = []
    for t in texts:
        r = requests.post(OLLAMA_EMBED_URL, json={"model": EMBED_MODEL, "prompt": t}, timeout=60)
        r.raise_for_status()
        vectors.append(r.json()["embedding"])
    return np.array(vectors, dtype=np.float32)

def build():
    os.makedirs("data", exist_ok=True)
    raw = "data/raw_pages.jsonl"
    meta_path = "data/meta.json"
    index_path = "data/faiss.index"

    chunks, meta = [], []
    with open(raw, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            url, text = rec["url"], rec["text"]
            for ci, c in enumerate(chunk(text)):
                chunks.append(c)
                meta.append({"url": url, "chunk_id": ci})

    print("Total chunks:", len(chunks))

    vecs = []
    bs = 32  # smaller batch because local embeddings are heavier
    for i in range(0, len(chunks), bs):
        batch = chunks[i:i+bs]
        v = embed_texts(batch)
        vecs.append(v)
        print("Embedded", min(i+bs, len(chunks)), "/", len(chunks))

    X = np.vstack(vecs)
    faiss.normalize_L2(X)

    index = faiss.IndexFlatIP(X.shape[1])
    index.add(X)

    faiss.write_index(index, index_path)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({"chunks": chunks, "meta": meta}, f, ensure_ascii=False)

    print("Saved:", index_path, meta_path)

if __name__ == "__main__":
    build()