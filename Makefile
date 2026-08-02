.PHONY: install run static demo test eval check

install:
	python3 -m pip install -e '.[dev]'

run:
	python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

static:
	python3 -m http.server 8766 --directory web

demo:
	./scripts/demo.sh

test:
	python3 -m pytest -q

eval:
	python3 scripts/evaluate.py

check:
	./scripts/check.sh
