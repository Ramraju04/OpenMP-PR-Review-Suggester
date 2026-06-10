import os
import json
import requests
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer
from time import sleep

GITHUB_TOKEN = os.getenv("COMPILER_DESIGN_GITHUB_TOKEN")
REPO_OWNER = "llvm"  # Change as needed
REPO_NAME = "llvm-project"  # Change as needed
LABEL = "openmp"
PER_PAGE = 50
TARGET_NUM_PRS = 500

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

model = SentenceTransformer('all-MiniLM-L6-v2')

def fetch_prs(page=1):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    params = {
        "state": "closed",  # or 'all' if you want open and closed PRs
        "per_page": PER_PAGE,
        "page": page,
        "labels": LABEL,
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def fetch_pr_reviews(pr_number):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/reviews"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    reviews = response.json()
    reviewers = set()
    for review in reviews:
        if review.get("user") and review["user"].get("login"):
            reviewers.add(review["user"]["login"])
    return list(reviewers)

def fetch_pr_files(pr_number):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/files"
    files = []
    page = 1
    while True:
        params = {"per_page": 100, "page": page}
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        files.extend([f["filename"] for f in data])
        if len(data) < 100:
            break
        page += 1
    return files

def get_pr_embedding(title, body, changed_files):
    combined_text = title + "\n" + (body or "") + "\nFiles: " + ", ".join(changed_files)
    embedding = model.encode(combined_text)
    return embedding

def parse_datetime(dt_str):
    if dt_str:
        return datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")
    return None

def fetch_and_store_pr_data(output_file="pr_data.json", target_num_prs=500):
    all_prs = []
    page = 1  

    while len(all_prs) < target_num_prs:
        print(f"\nFetching page {page}...")
        prs = fetch_prs(page) 
        if not prs:
            print(f"No more PRs found on page {page}. Ending scan.")
            break

        for pr in prs:
            labels = [label["name"] for label in pr.get("labels", [])]
            if not any("openmp" in label.lower() for label in labels):
                continue

            pr_number = pr["number"]
            print(f"   🔍 Processing PR #{pr_number}...")

            reviewers = fetch_pr_reviews(pr_number)
            changed_files = fetch_pr_files(pr_number)
            merged_at = parse_datetime(pr.get("merged_at"))

            embedding = get_pr_embedding(pr["title"], pr.get("body", ""), changed_files)

            pr_data = {
                "number": pr_number,
                "title": pr["title"],
                "body": pr.get("body", ""),
                "reviewers": reviewers,
                "labels": labels,
                "changed_files": changed_files,
                "merged_at": merged_at.isoformat() if merged_at else None,
                "embedding": embedding.tolist(),
            }

            all_prs.append(pr_data)
            print(f"      ➕ Total PRs collected so far: {len(all_prs)}")

            if len(all_prs) >= target_num_prs:
                break

            sleep(0.5)  

      
        with open(output_file, "w") as f:
            json.dump(all_prs, f, indent=2)

        page += 1 

    print(f"\nsaved {len(all_prs)} PRs to {output_file}")

if __name__ == "__main__":
    fetch_and_store_pr_data()  # Adjust max_pages as needed
