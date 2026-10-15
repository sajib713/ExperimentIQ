PYTHON ?= python
export PYTHONPATH=src
.PHONY: test acquire run postgres dashboard
acquire:
	$(PYTHON) -m experimentiq.cli acquire
run:
	$(PYTHON) -m experimentiq.cli all
postgres:
	docker compose up -d postgres
load-db:
	$(PYTHON) -m experimentiq.cli load-db
dashboard:
	$(PYTHON) -m http.server 8000 -d dashboard
test:
	$(PYTHON) -m pytest -q
