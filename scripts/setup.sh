#!/usr/bin/env bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env || true
echo
echo "Edit .env to add your SLACK_WEBHOOK."
echo "Done."
