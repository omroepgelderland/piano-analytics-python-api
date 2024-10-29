#!/bin/bash

# Builds dist package files and a new git tag for the current commit.

function delete_dist_files() {
    rm -rf \
        dist/
}

projectdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$projectdir" || exit 1

./set-env.sh || exit 1

oude_versie=$(hatch version)
echo "De huidige versie is $oude_versie. Nieuwe versie? "
read -r nieuwe_versie
git_versie="v$nieuwe_versie"
git tag "$git_versie"

delete_dist_files
python3 -m build || exit 1
python3 -m twine upload --repository testpypi dist/* || exit 1
