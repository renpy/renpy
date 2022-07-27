#!/bin/bash

set -e -u -o pipefail

branch=$(git branch --show-current)
git checkout master
git pull --rebase
git merge $branch -m "Merge branch '$branch'"
git push
git checkout $branch
