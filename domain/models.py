import socket


from service_flower import states
from service_flower.client import FlowerClient

from time_execution.decorator import write_metric

SHORT_HOSTNAME = socket.gethostname()


class Monitor(object):
    def __init__(self):
        self.client = FlowerClient()

    def get_tasks_count(self):
        taskname = 'inspirehep.modules.orcid.tasks.orcid_push'
        result = {}
        for state in states.ALL_STATES:
            response = self.client.get_tasks(state=state, taskname=taskname, limit=None)
            response.raise_for_result()
            result[state] = len(response)
            self._write_metric(
                count=len(response),
                state=state,
                name=taskname,
            )
        return result

    def _write_metric(self, **kwargs):
        data = dict(
            hostname=SHORT_HOSTNAME,
            origin='inspire-orcidpush-monitoring',
            name='default',
        )
        data.update(kwargs)
        write_metric(**data)
