import os
import service_flower.conf
import time_execution

from pprint import pprint

from time_execution.backends.threaded import ThreadedBackend
from time_execution.backends.elasticsearch import ElasticsearchBackend

from domain.models import Monitor


def configure():
    d = dict(
        BASE_URL='https://inspire-prod-worker3-task1.cern.ch/api',
        REQUEST_TIMEOUT=30,
        HTTP_AUTH_USERNAME=os.environ['FLOWER_USERNAME'],
        HTTP_AUTH_PASSWORD=os.environ['FLOWER_PASSWORD'],
    )
    service_flower.conf.settings.configure(**d)

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
    async_es_metrics = ThreadedBackend(
        ElasticsearchBackend,
        backend_kwargs=dict(
            hosts=APPMETRICS_ELASTICSEARCH_HOSTS,
            index=INDEX_NAME),
    )
    time_execution.settings.configure(
        backends=[async_es_metrics],
        # hooks=(status_code_hook,),
        origin='inspire_next'
    )


if __name__ == '__main__':
    configure()
    print('** ORCIDPUSH MONITOR **')
    monitor = Monitor()
    result = monitor.get_tasks_count()
    print('TASK COUNT')
    pprint(result)
    print('END')
