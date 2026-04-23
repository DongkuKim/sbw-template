PYTHON ?= python3

.PHONY: validate test

validate:
	$(PYTHON) .sbw-template/scripts/validate_specs.py .

test:
	$(PYTHON) -m unittest discover -s .sbw-template/tests -p 'test_*.py'
