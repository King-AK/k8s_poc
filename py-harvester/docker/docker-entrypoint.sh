#!/bin/sh

set -e

## activate our virtual environment here
#. /opt/pysetup/.venv/bin/activate

# You can put other setup logic here
poetry install
poetry run python py_harvester/main.py "$@"

## Evaluating passed command:
#exec "$@"