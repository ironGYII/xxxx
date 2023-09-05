import json


class Machine:

    def __init__(self, machine_id, pub_key, host, port, server_info, api_version):
        if type(server_info) == str and len(server_info) > 0:
            server_info = json.loads(server_info)
        else:
            server_info = None
        self.machine_id = machine_id
        self.pub_key = pub_key
        self.host = host
        self.port = port
        self.server_info = server_info
        self.api_version = api_version

    @property
    def data(self):
        return dict(machine_id=self.machine_id, pub_key=self.pub_key, host=self.host, port=self.port, server_info=self.server_info, apiVersion=self.api_version)


class MountedMachine:

    _machines = dict()

    def __init__(self):
        pass

    def register(self, machine):
        self._machines[machine.pub_key] = self._machines.get(machine.pub_key, []) + [machine]

        for m in self._machines.get(machine.pub_key, []):
            if m.machine_id == machine.machine_id:
                raise Exception("machine_id exit")


mounted_machine = MountedMachine()