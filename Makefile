.PHONY: help init run build test clean

help:
	@echo ""
	@echo "Phoenix Hub"
	@echo ""
	@echo "make init"
	@echo "make run"
	@echo "make build"
	@echo "make test"
	@echo "make clean"

init:
	python3 -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r apps/api/requirements.txt
	cd apps/web && npm install

run:
	. .venv/bin/activate && export PYTHONPATH=apps/api/src && uvicorn app.main:app --host 0.0.0.0 --port 8000

build:
	cd apps/web && npm install && npm run build
	. .venv/bin/activate && python -m compileall apps/api/src

test:
	. .venv/bin/activate && pytest tests -q

clean:
	rm -rf .venv apps/web/node_modules apps/web/dist
	find apps/api/src -type d -name '__pycache__' -prune -exec rm -rf {} +