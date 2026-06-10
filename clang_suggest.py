# clang_suggest.py

import argparse
from suggest import main as suggest_main  # your existing script already has `main()`

def cli_main():
    parser = argparse.ArgumentParser(
        description="Clang-style CLI for suggesting reviewers for LLVM PRs."
    )
    parser.add_argument("pr", type=int, help="Pull request number")
    args = parser.parse_args()

    # Use the llvm-project repo by default
    suggest_main("llvm/llvm-project", args.pr)

if __name__ == "__main__":
    cli_main()