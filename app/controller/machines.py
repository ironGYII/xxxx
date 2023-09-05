class Machine:

    def __init__(self, pub_key, ip, container_name, info):
        self._pub_key = pub_key
        self._ip = ip
        self._container_name = container_name
        self._info = info

    @property
    def data(self):
        data = dict()
        data.update(self._info)
        data["pub_key"] = self._pub_key
        data["ip"] = self._ip
        data["info"] = self._info
        return  data

    @property
    def name(self):
        return self._container_name


class MountedMachine:

    _machines = dict()

    def __init__(self):
        pass

    def register(self, machine):
        self._machines[machine.name] = machine



mounted_machine = MountedMachine()