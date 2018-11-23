# Inspire ORCID push infra monitoring

Usage:
```bash
$ export APPMETRICS_ELASTICSEARCH_USERNAME=myuser
$ export APPMETRICS_ELASTICSEARCH_PASSWORD=mypass 
$ export FLOWER_USERNAME=myuser 
$ export FLOWER_PASSWORD=mypass 
$ export RABBIT_USERNAME=myuser 
$ export RABBIT_PASSWORD=mypass 
# Then:
$ pip install -r requirements/requirements-base.txt
$ python orcidpushinfra_monitor.py prod
# Or with the Makefile:
$ make venv
$ make prod
```
