.PHONY: setup run test eval seed index

setup:
	python -m venv .venv
	.venv/bin/pip install -r backend/requirements.txt || .venv/Scripts/pip install -r backend/requirements.txt
	cd frontend && npm install

run:
	@echo "TODO: start FastAPI and Next.js together (or use docker compose up)"

test:
	cd backend && python -m pytest -q

eval:
	python eval/run_eval.py

seed:
	python scripts/seed_db.py

index:
	python scripts/build_index.py
