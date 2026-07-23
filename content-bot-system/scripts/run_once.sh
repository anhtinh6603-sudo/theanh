#!/usr/bin/env bash
# Runs the full pipeline once, from the project's own venv.
set -euo pipefail
cd "$(dirname "$0")/.."
source .venv/bin/activate
python pipeline.py --all
