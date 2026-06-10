from typing import List, Optional
from datetime import datetime

class PullRequest:
    def __init__(
        self,
        number: int,
        title: str,
        body: str,
        changed_files: List[str],
        reviewers: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        merged_at: Optional[str] = None,
    ):
        self.number = number
        self.title = title
        self.body = body
        self.changed_files = changed_files
        self.reviewers = reviewers or []
        self.labels = labels or []
        self.merged_at = (
            datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ") if merged_at else None
        )

    def __repr__(self):
        return (
            f"PR #{self.number}: {self.title}\n"
            f"Labels: {self.labels}\n"
            f"Reviewers: {self.reviewers}\n"
            f"Files changed: {len(self.changed_files)} files\n"
            f"Merged at: {self.merged_at}\n"
        )
