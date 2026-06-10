import requests
import time
import os

GITHUB_TOKEN = os.getenv("COMPILER_DESIGN_GITHUB_TOKEN")  # Set this in your terminal before running
REPO = "llvm/llvm-project"  # Change if you're using another repo

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_openmp_prs(max_prs=50):
    prs = []
    page = 1

    while len(prs) < max_prs:
        print(f"Fetching page {page}...")
        url = f"https://api.github.com/repos/{REPO}/pulls"
        params = {
            "state": "closed",
            "per_page": 100,
            "page": page,
        }

        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch PRs: {response.status_code} {response.text}")

        data = response.json()
        if not data:
            break

        for pr in data:
            if 'openmp' in [label['name'].lower() for label in pr.get("labels", [])]:
                prs.append({
                    "number": pr["number"],
                    "title": pr["title"],
                    "body": pr["body"],
                    "user": pr["user"]["login"],
                    "merged_at": pr["merged_at"],
                    "labels": [label["name"] for label in pr["labels"]],
                    "url": pr["html_url"]
                })

            if len(prs) >= max_prs:
                break

        page += 1
        time.sleep(1)

    return prs


def fetch_changed_files(pr_number):
    url = f"https://api.github.com/repos/{REPO}/pulls/{pr_number}/files"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error fetching files for PR #{pr_number}")
        return []

    files = response.json()
    return [file["filename"] for file in files]


if __name__ == "__main__":
    prs = fetch_openmp_prs(10)  # Fetch 10 PRs for now
    for pr in prs:
        changed_files = fetch_changed_files(pr["number"])
        pr["files"] = changed_files
        print(f"\nPR #{pr['number']}: {pr['title']}")
        print(f"Files changed: {changed_files}")
