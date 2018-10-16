DEPS:=requirements/requirements-base.txt
VIRTUALENV=$(shell which virtualenv)
PIP:="venv/bin/pip"
CMD_FROM_VENV:=". venv/bin/activate; which"
PYTHON=$(shell "$(CMD_FROM_VENV)" "python2.7")

.PHONY: venv run

default: run;

venv:
ifneq ($(shell ls venv/bin/python),venv/bin/python)
	$(VIRTUALENV) -p $(shell which python2.7) venv
	@. venv/bin/activate
	@$(PIP) install -U "pip>=18.0" -q
	@$(PIP) install -r $(DEPS)
else
	echo 'venv already exists'
endif

pyclean:
	@find . -name *.pyc -delete

clean: pyclean
	@rm -rf venv

run: venv
	@$(PYTHON) orcidpush_monitor.py
