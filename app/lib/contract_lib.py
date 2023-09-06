import json
import time
from app.lib.config import role
from app.lib.conn import helper_contract, get_nonce, transaction
from app.model.machine import Machine, Price


class UserInfo:
    def __init__(self, address, balance, provider_blocked_funds, recipient_blocked_funds, info):
        if type(info) == str and len(info) > 0:
            info = json.loads(info)
        self.address = address
        self.balance = balance
        self.provider_blocked_funds = provider_blocked_funds
        self.recipient_blocked_funds = recipient_blocked_funds
        self._info = info

    @classmethod
    def from_contract(cls, address):
        info = contract_helper.get_account_info(addr=address)

    @property
    def info(self):
        return dict(address=self.address, balance=self.balance, provider_blocked_funds=self.provider_blocked_funds, recipient_blocked_funds=self.recipient_blocked_funds, info=self._info)

class HelperLib:
    _contract = None

    def __init__(self):
        self._contract = helper_contract

    def list_devices(self, _limit, _offset):
        resp = self._contract.functions.listDevices().call()
        result = [Machine.init_from_contract(item) for item in resp]
        return result

    def list_own_devices(self, _provider, _limit, _offset):
        resp = self._contract.functions.listOwnDevices(_provider.public_key, 10, 0).call()
        resp = list(filter(lambda x: x[0] != 0, resp))
        result = [Machine.init_from_contract(item) for item in resp]
        return result

    def listLease(self, _user, _limit, _offset):
        pass

    def online_server(self, _user, machine_info, price, start_time, end_time):
        # print(dict(_machineId=machine_info.machine_id, _serverInfo=machine_info.contract_server_info, _price=price.contract_price, _startTime=start_time, _endTime=end_time))
        tx_receipt = transaction(_user, self._contract.functions.onlineServer(_machineId=machine_info.machine_id, _serverInfo=machine_info.contract_server_info, _price=price.contract_price, _startTime=start_time, _endTime=end_time))
        return tx_receipt

    # 质押单位是ETH
    def stake(self, _user, amount):
        tx_receipt = transaction(_user, self._contract.functions.stake(), value=int(amount * 10 ** 18))
        return tx_receipt

    def unstake(self, _user, amount):
        tx_receipt = transaction(_user, self._contract.functions.unstake(amount=int(amount * 10 ** 18)))
        return tx_receipt

    def register(self, addr):
        tx_receipt = transaction(addr, self._contract.functions.register())
        return tx_receipt

    def get_account_info(self, addr):
        address, balance, provider_blocked_funds, recipient_blocked_funds, info = self._contract.functions.getAccount(addr.public_key).call()
        return UserInfo(address, balance, provider_blocked_funds, recipient_blocked_funds, info)

    def set_provider_info(self, addr, _info):
        tx_receipt = transaction(addr, self._contract.functions.setProviderInfo(_info))
        return tx_receipt


contract_helper = HelperLib()


if __name__ == '__main__':
    print(HelperLib().register(role.provider))
    print(HelperLib().get_account_info(role.provider).info)
    import json
    print(HelperLib().set_provider_info(role.provider, json.dumps(dict(a=1, b=2))))
    print(HelperLib().get_account_info(role.provider).info)

    # print(HelperLib().stake(role.provider, 33))
    # print(HelperLib().unstake(role.provider, 10))

    # print(HelperLib().online_server(role.provider, Machine(machine_id="ym-test", pub_key=role.provider.public_key, host="127.0.0.1", port="10", server_info=dict(a="a", b="b", c="c"), api_version="v0"), price=Price(server_price=10 ** 16, storage_price=10, upband_width=20, downband_width=30), start_time=int(time.time()), end_time=int(time.time()) + 10))
    print([i.data for i in HelperLib().list_devices(10, 0)])
    print([i.data for i in HelperLib().list_own_devices(role.provider, 10, 0)])
