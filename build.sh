#!/bin/bash

# Builds dist package files and a new git tag for the current commit.

function delete_dist_files() {
    rm -rf \
        dist/ \
        src/piano_analytics_api/_version.py
}

projectdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# projectnaam="$(basename "$projectdir")"
# tempdir="/tmp/dist_$projectnaam/"
cd "$projectdir" || exit 1

./set-env.sh || exit 1
source env/bin/activate || exit 1

if ! git status --porcelain=v1 2>/dev/null | wc -l; then
    git status
    echo "There are uncommitted changes."
    exit 1
fi

head_version=$(git tag --points-at HEAD)
if [[ $head_version != "" ]]; then
    echo "HEAD is on existing version $head_version. Make a new commit to publish a new version"
    exit 1
fi

prev_version="$(git tag --list 'v*' --sort=v:refname | tail -n1)"
echo -e "\nThe latest version is $prev_version. New version (without v)? "
read -r new_version
git_version="v$new_version"
git tag "$git_version"
git push
git push origin "$git_version"

python3 -m build || exit 1
python3 -m twine upload dist/*-"$new_version"* || exit 1
