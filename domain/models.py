import socket


from service_flower import states
from service_flower.client import FlowerClient
from service_rabbit.client import RabbitClient

from time_execution.decorator import write_metric

SHORT_HOSTNAME = socket.gethostname()


class Monitor(object):
    def __init__(self):
        self.flower_client = FlowerClient()
        self.rabbit_client = RabbitClient()

    def get_celery_tasks_count(self):
        taskname = 'inspirehep.modules.orcid.tasks.orcid_push'
        result = {}
        for state in states.ALL_STATES:
            response = self.flower_client.get_tasks(state=state, taskname=taskname, limit=None)
            response.raise_for_result()
            result[state] = len(response)
            self._write_metric(
                count=len(response),
                state=state,
                name=taskname,
            )
        return result

    def get_rabbit_messages_and_consumers_count(self):
        response = self.rabbit_client.get_queue('inspire', 'orcid_push')
        response.raise_for_result()
        consumers = response.get_consumers_count()
        messages = response.get_messages_count()

        self._write_metric(
            count=messages,
            name='rabbit-queue-orcid_push-messages-count',
        )
        self._write_metric(
            count=consumers,
            name='rabbit-queue-orcid_push-counsumers-count',
        )
        return messages, consumers

    def _write_metric(self, name='default', **kwargs):
        data = dict(
            hostname=SHORT_HOSTNAME,
            origin='inspire-orcidpush-monitoring',
            name=name,
        )
        data.update(kwargs)
        write_metric(**data)
