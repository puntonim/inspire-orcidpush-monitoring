DEPS:=requirements/requirements-base.txt
VIRTUALENV=$(shell which virtualenv)
PIP:="venv/bin/pip"
CMD_FROM_VENV:=". venv/bin/activate; which"
PYTHON=$(shell "$(CMD_FROM_VENV)" "python2.7")

.PHONY: venv run requirements

default: run;

venv:
	$(VIRTUALENV) -p $(shell which python2.7) venv
	. venv/bin/activate
	$(PIP) install -U "pip>=18.0" -q
	$(PIP) install -r $(DEPS)

requirements:
	pip install -U -r requirements.txt

pyclean:
	find . -name *.pyc -delete

clean: pyclean
	rm -rf venv

run:
	$(PYTHON) orcidpush_monitor.py

cleanpipcache:
	rm -rf ~/Library/Caches/pip
