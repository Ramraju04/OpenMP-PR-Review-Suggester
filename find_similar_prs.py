import json
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import os

# Configuration
GITHUB_TOKEN = os.getenv("COMPILER_DESIGN_GITHUB_TOKEN")  # Set this in your .env or shell
MODEL_NAME = "all-MiniLM-L6-v2"
PR_DATA_FILE = "pr_data.json"
EMBEDDINGS_FILE = "pr_embeddings.npy"
TOP_K = 5  # Number of similar PRs to return

# Headers for GitHub API
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

model = SentenceTransformer(MODEL_NAME)

def fetch_pr(repo, pr_number):
    # print(os.getenv("COMPILER_DESIGN_GITHUB_TOKEN"))
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def fetch_pr_files(repo, pr_number):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return [f["filename"] for f in response.json()]

def create_text_blob(pr, files):
    title = pr.get("title", "")
    body = pr.get("body", "")
    return f"{title}\n{body}\nFiles: {' '.join(files)}"

def load_historical_data():
    with open(PR_DATA_FILE, "r") as f:
        pr_data = json.load(f)
    embeddings = np.load(EMBEDDINGS_FILE)
    return pr_data, embeddings

def find_similar_prs(new_embedding, all_embeddings, k=5):
    similarities = cosine_similarity([new_embedding], all_embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:k]
    return top_indices, similarities[top_indices]

def main(repo, pr_number):
    print(f"\n Fetching PR #{pr_number} from {repo}...")
    pr = fetch_pr(repo, pr_number)
    files = fetch_pr_files(repo, pr_number)
    text_blob = create_text_blob(pr, files)
    new_embedding = model.encode([text_blob])[0]

    print(" Loading historical PR data and embeddings...")
    pr_data, embeddings = load_historical_data()

    # ✅ Filter PRs with 'openmp' label only
    filtered = [(i, pr) for i, pr in enumerate(pr_data)
                if any('openmp' in lbl.lower() for lbl in pr.get("labels", [])) and pr["number"] != pr_number]
    
    if not filtered:
        print(" No PRs found with the 'openmp' label.")
        return

    indices, filtered_pr_data = zip(*filtered)
    filtered_embeddings = np.array([embeddings[i] for i in indices])

    print(" Finding similar PRs...")
    top_indices, top_scores = find_similar_prs(new_embedding, filtered_embeddings, TOP_K)

    print("\n Top Similar PRs and Reviewers:")
    for i, idx in enumerate(top_indices):
        pr_entry = filtered_pr_data[idx]
        print(f"\n#{i+1} - PR #{pr_entry['number']}")
        print(f"   - Title     : {pr_entry['title']}")
        print(f"   - Similarity: {top_scores[i]:.4f}")
        print(f"   - Reviewers : {', '.join(pr_entry['reviewers']) if pr_entry['reviewers'] else 'None'}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Find similar PRs and reviewers.")
    parser.add_argument("--repo", required=True, help="GitHub repo in owner/name format")
    parser.add_argument("--pr", type=int, required=True, help="PR number to analyze")
    args = parser.parse_args()

    main(args.repo, args.pr)
