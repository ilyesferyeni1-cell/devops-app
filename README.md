# DevOps App - by Ilyes
A small Python app to learn DevOps.

Maintained by ilyes
## How to run
python3 app.py

Current version: 1.0.0

## Health check
health() returns the app status and version.
Run: python3 app.py
Quick Friday fix

## Setup (after cloning)
pre-commit install    # activate the commit guards (once per clone)

## Run the tests
pip install -r requirements-dev.txt
pytest --cov=app --cov-report=term-missing --cov-fail-under=90 --junitxml=report.xml
