import json
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm

# Load pre-trained model (you can change this to another one on HuggingFace)
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

# Input & output paths
INPUT_JSON = "pr_data.json"
OUTPUT_EMBEDDING_FILE = "pr_embeddings.npy"
OUTPUT_TEXTS_FILE = "pr_texts.json"

def create_text_blob(pr):
    """
    Combine PR metadata into a single text blob.
    """
    title = pr.get("title", "")
    body = pr.get("body", "")
    files = pr.get("changed_files", [])
    return f"{title}\n{body}\nFiles: {' '.join(files)}"

def main():
    with open(INPUT_JSON, "r") as f:
        pr_data = json.load(f)

    print(f"📄 Loaded {len(pr_data)} PRs from {INPUT_JSON}")

    texts = []
    for pr in pr_data:
        blob = create_text_blob(pr)
        texts.append(blob)

    print("🔍 Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    # Save embeddings and associated text
    np.save(OUTPUT_EMBEDDING_FILE, embeddings)
    with open(OUTPUT_TEXTS_FILE, "w") as f:
        json.dump(texts, f, indent=2)

    print(f"✅ Saved {len(embeddings)} embeddings to {OUTPUT_EMBEDDING_FILE}")
    print(f"📝 Saved input texts to {OUTPUT_TEXTS_FILE}")

if __name__ == "__main__":
    main()
