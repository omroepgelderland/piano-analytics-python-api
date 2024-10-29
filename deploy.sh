#!/bin/bash

function delete_dist_bestanden() {
    rm -rf \
        dist/
}

if [[ $1 == "" ]]; then
    mode="dev"
else
    mode="$1"
fi
projectdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# projectnaam="$(basename "$projectdir")"
cd "$projectdir" || exit 1

if [ ! -d "env" ]; then
    python3 -m venv env || exit 1
fi
source env/bin/activate || exit 1
python3 -m pip install --upgrade pip
pip3 install -r dev-requirements.txt || exit 1

if [[ $mode == "production" ]]; then
    oude_versie=$(hatch version)
    echo "De huidige versie is $oude_versie. Nieuwe versie? "
    read -r nieuwe_versie
    git_versie="v$nieuwe_versie"
    git tag "$git_versie"

    delete_dist_bestanden
    python3 -m build || exit 1
    python3 -m twine upload --repository testpypi dist/* || exit 1
fi
