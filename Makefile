.PHONY: setup run test eval seed index docker-up docker-down

setup:
	python -m venv .venv
	.venv/bin/pip install -r backend/requirements.txt || .venv/Scripts/pip install -r backend/requirements.txt
	cd frontend && npm install

run-backend:
	uvicorn backend.app.main:app --reload --port 8000 --app-dir .

run-frontend:
	cd frontend && npm run dev

run:
	@echo "To run both servers, open two terminals:"
	@echo "Terminal 1: make run-backend (or uvicorn backend.app.main:app --reload --port 8000)"
	@echo "Terminal 2: make run-frontend (or cd frontend && npm run dev)"

test:
	python -m pytest backend/tests/ -v

eval:
	python eval/run_eval.py

seed:
	python scripts/seed_db.py

index:
	python scripts/build_index.py

tamper-demo:
	python scripts/tamper_demo.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down
