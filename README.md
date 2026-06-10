# OpenMP PR Review Suggester

A machine learning powered reviewer recommendation system for LLVM OpenMP pull requests.

The project analyzes historical OpenMP pull requests, generates semantic embeddings using Sentence Transformers, and recommends reviewers for new pull requests by finding similar past contributions.

## Features

- Fetches OpenMP-related PRs from LLVM GitHub repository
- Extracts PR metadata, labels, reviewers, and changed files
- Generates semantic embeddings using Sentence Transformers
- Finds similar historical pull requests
- Suggests potential reviewers based on previous review patterns
- GitHub API integration

---

## Project Structure

```
OpenMP-PR-Review-Suggester/
│
├── github_api.py
├── pr_data.py
├── pr_data_store.py
├── prepare_embedding_index.py
├── find_similar_prs.py
├── clang_suggest.py
├── README.md
└── .gitignore
```

---

## Requirements

- Python 3.9+
- GitHub Personal Access Token

### Python Packages

```bash
pip install requests numpy scikit-learn sentence-transformers tqdm
```

---

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/OpenMP-PR-Review-Suggester.git
cd OpenMP-PR-Review-Suggester
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

---

### 3. Configure GitHub Token

Windows:

```powershell
$env:COMPILER_DESIGN_GITHUB_TOKEN="your_token_here"
```

Linux/macOS:

```bash
export COMPILER_DESIGN_GITHUB_TOKEN="your_token_here"
```

---

## Usage

### Step 1: Fetch Historical PR Data

```bash
python pr_data_store.py
```

Generates:

- pr_data.json

---

### Step 2: Generate Embeddings

```bash
python prepare_embedding_index.py
```

Generates:

- pr_embeddings.npy
- pr_texts.json

---

### Step 3: Find Similar Pull Requests

```bash
python find_similar_prs.py
```

or

```bash
python clang_suggest.py <PR_NUMBER>
```

Example:

```bash
python clang_suggest.py 123456
```

---

## Workflow

1. Collect historical OpenMP PRs.
2. Generate text embeddings.
3. Fetch a target PR.
4. Compute similarity against historical PRs.
5. Recommend reviewers based on similar PRs.

---

## Technologies Used

- Python
- GitHub REST API
- Sentence Transformers
- NumPy
- Scikit-Learn
- LLVM/OpenMP Dataset

---

## Future Improvements

- Reviewer ranking score
- Web dashboard
- Fine-tuned embedding model
- Reviewer workload balancing
- Real-time GitHub Action integration

---

## License

MIT License

---

## Author

Ramraju
