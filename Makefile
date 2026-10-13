PYTHON ?= python
.PHONY: test theory analyze audit tables selection

test:
	$(PYTHON) -m pytest -q

theory:
	$(PYTHON) src/theory.py --N 0 9 18 26 35 42 --a 0.28 --alpha 0.2 --horizons 1 3 6

analyze:
	@for exp in long-horizon-clipping external-datasets validation-locked-selection; do $(PYTHON) -m src.reanalyze --experiment $$exp; done

selection:
	$(PYTHON) -m src.selection_diagnostics

audit:
	@for file in results/archives/long_horizon_clipping.tar.gz results/archives/external_datasets.tar.gz results/archives/validation_locked_selection.tar.gz; do $(PYTHON) src/audit_releases.py --archive $$file; done

tables: analyze
	$(PYTHON) -m src.manuscript_tables
