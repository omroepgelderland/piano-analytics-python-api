#!/bin/bash

set -euo pipefail

projectdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# projectnaam="$(basename "$projectdir")"
# tempdir="/tmp/dist_$projectnaam/"
cd "$projectdir"

if [ ! -d "env" ]; then
    python3 -m venv env
fi
env/bin/python3 -m pip install --upgrade pip | { grep -v 'already satisfied' || :; }
env/bin/pip3 install \
    --upgrade \
    -r requirements.txt \
    -r dev-requirements.txt \
    | { grep -v 'already satisfied' || :; }

env/bin/ruff check --fix . || env/bin/ruff check . || :
env/bin/ruff format . || env/bin/ruff format --check .
