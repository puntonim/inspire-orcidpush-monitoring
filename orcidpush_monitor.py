import os
import service_flower.conf
import service_rabbit.conf
import time_execution

from pprint import pprint

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


if __name__ == '__main__':
    configure()
    print('** ORCIDPUSH MONITOR **')
    monitor = Monitor()

    result = monitor.get_celery_tasks_count()
    print('CELERY TASK COUNT')
    pprint(result)

    result = monitor.get_rabbit_messages_and_consumers_count()
    print('\nRABBIT QUEUE SIZE for queue "orcid_push"')
    print('#messages={}\n#consumers={}'.format(*result))

    print('**END**')
