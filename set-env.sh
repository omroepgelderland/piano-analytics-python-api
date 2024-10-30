#!/bin/bash

# Sets up the virtualenv and installs dev dependencies.

projectdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# projectnaam="$(basename "$projectdir")"
cd "$projectdir" || exit 1

if [ ! -d "env" ]; then
    python3 -m venv env || exit 1
fi
source env/bin/activate || exit 1
python3 -m pip install --upgrade pip | grep -v 'already satisfied'
pip3 install -r dev-requirements.txt | grep -v 'already satisfied'
if [[ ! ${PIPESTATUS[0]} -eq 0 ]]; then
    exit 1
fi
