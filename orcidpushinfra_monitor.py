import os
import sys
import warnings

import click
import time_execution

import service_flower.conf
import service_rabbit.conf
from time_execution.backends.elasticsearch import ElasticsearchBackend

from domain.models import Monitor


# Ignore warnings like:
# ...http_urllib3.py:135: UserWarning: Connecting to inspire-qa-logs-client1.cern.ch
# using SSL with verify_certs=False is insecure.
if not sys.warnoptions:
    msg = r'Connecting to .* using SSL with verify_certs=False is insecure.'
    warnings.filterwarnings('ignore', message=msg, module='.*http_urllib3.*')


def configure():
    d = dict(
        BASE_URL='https://inspire-prod-worker3-task1.cern.ch/api',
        REQUEST_TIMEOUT=30,
        HTTP_AUTH_USERNAME=os.environ['FLOWER_USERNAME'],
        HTTP_AUTH_PASSWORD=os.environ['FLOWER_PASSWORD'],
    )
    service_flower.conf.settings.configure(**d)

    d = dict(
        BASE_URL='http://inspire-prod-broker1.cern.ch:15672/api',
        REQUEST_TIMEOUT=30,
        HTTP_AUTH_USERNAME=os.environ['RABBIT_USERNAME'],
        HTTP_AUTH_PASSWORD=os.environ['RABBIT_PASSWORD'],
    )
    service_rabbit.conf.settings.configure(**d)

    APPMETRICS_ELASTICSEARCH_KWARGS = dict(
        port=443,
        http_auth=(
            os.environ['APPMETRICS_ELASTICSEARCH_USERNAME'],
            os.environ['APPMETRICS_ELASTICSEARCH_PASSWORD']),
        use_ssl=True,
        verify_certs=False,
    )
    APPMETRICS_ELASTICSEARCH_HOSTS = [
        dict(host='inspire-prod-logs-client1.cern.ch',
             **APPMETRICS_ELASTICSEARCH_KWARGS),
        dict(host='inspire-prod-logs-client2.cern.ch',
             **APPMETRICS_ELASTICSEARCH_KWARGS),
    ]
    INDEX_NAME='inspiremonitoring-prod'
    backend = ElasticsearchBackend(
        hosts=APPMETRICS_ELASTICSEARCH_HOSTS,
        index=INDEX_NAME
    )
    time_execution.settings.configure(
        backends=[backend],
        # hooks=(status_code_hook,),
        origin='inspire_next'
    )


@click.group()
def cli():
    pass


@click.command()
def prod():
    perform_monitoring('prod')


@click.command()
def qa():
    click.echo('Not implemented yet!')


cli.add_command(prod)
cli.add_command(qa)


def perform_monitoring(env):
    configure()
    monitor = Monitor()
    monitor.get_celery_tasks_count()
    monitor.get_rabbit_messages_and_consumers_count()


if __name__ == '__main__':
    click.echo('** INSPIRE ORCID PUSH INFRA MONITOR **')
    cli()
