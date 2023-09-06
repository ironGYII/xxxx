import json


class Price:

    def __init__(self, server_price, storage_price, upband_width, downband_width):
        self.server_price = server_price # Wei / s
        self.storage_price = storage_price
        self.upband_width = upband_width
        self.downband_width = downband_width

    @classmethod
    def init_from_contract(cls, resp):
        return Price(*resp)


    @property
    def contract_price(self):
        return (self.server_price, self.storage_price, self.upband_width, self.downband_width)


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
        self.status = 0  # Created
        self.price = None
        self.market_id = 0

    @classmethod
    def init_from_contract(cls, resp):
        cid, address, status, machine_id, server_info, price = resp
        server_info = json.loads(server_info)
        print(server_info)
        machine = Machine(machine_id, address, server_info['host_info']['host'], server_info['host_info']['port'], server_info, server_info['api_version'])
        machine.price = Price.init_from_contract(price)
        return machine

    @property
    def data(self):
        return dict(machine_id=self.machine_id, pub_key=self.pub_key, host=self.host, port=self.port, server_info=self.server_info, apiVersion=self.api_version)

    # 生成合约的info
    @property
    def contract_server_info(self):
        from copy import copy
        data = copy(self.server_info) if self.server_info is not None else dict()
        data["api_version"] = self.api_version
        data["machine_id"] = self.machine_id
        data["host_info"] = dict(host=self.host, port=self.port)
        return json.dumps(data)
