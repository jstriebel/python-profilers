#!/bin/bash
set -eEuo pipefail

poetry run isort *.py
poetry run black *.py
