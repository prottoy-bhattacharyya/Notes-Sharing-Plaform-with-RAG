#!/usr/bin/env bash
set -e

read -e -p "Enter the repository name: " REPO_NAME

if [ -z "$REPO_NAME" ]; then
  echo "Repository name cannot be empty."
  exit 1
fi

# spaces -> hyphens, remove other invalid characters
REPO_NAME=$(echo "$REPO_NAME" | tr ' ' '-' | tr -cd 'A-Za-z0-9._-')
echo "Repository name: $REPO_NAME"

git init .
git add .
git commit -m "Initial commit"
git branch -M main

gh repo create "$REPO_NAME" --public --source=. --remote=origin
git push -u origin main