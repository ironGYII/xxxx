import json
import time

import web3

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

    # @classmethod
    # def from_contract(cls, address):
    #     info = contract_helper.get_account_info(addr=address)

    @property
    def info(self):
        return dict(address=self.address, balance=self.balance, provider_blocked_funds=self.provider_blocked_funds, recipient_blocked_funds=self.recipient_blocked_funds, info=self._info)


class HelperLib:
    _contract = None

    def __init__(self):
        self._contract = helper_contract

    def list_devices(self, _limit, _offset):
        resp = self._contract.functions.listDevices(_limit=_limit, _offset=_offset).call()
        result = [Machine.init_from_contract(item) for item in resp if item[0] != 0]
        return result

    def list_own_devices(self, _provider, _limit, _offset):
        resp = self._contract.functions.listOwnDevices(_provider.public_key, 10, 0).call()
        resp = list(filter(lambda x: x[0] != 0, resp))
        result = [Machine.init_from_contract(item) for item in resp]
        return result

    def list_provider_lease(self, public_key, _limit, _offset):
        lease, billing = self._contract.functions.listProviderLease(public_key, _limit, _offset).call()
        lease = list(filter(lambda x: x[1] != 0, lease))
        billing = list(filter(lambda x: x[1] != 0, billing))
        return lease, billing

    def online_server(self, _user, machine_info, price, start_time, end_time):
        # print(dict(_machineId=machine_info.machine_id, _serverInfo=machine_info.contract_server_info, _price=price.contract_price, _startTime=start_time, _endTime=end_time))
        tx_receipt = transaction(_user, self._contract.functions.onlineServer(_machineId=machine_info.machine_id, _serverInfo=machine_info.contract_server_info, _price=price.contract_price, _startTime=start_time, _endTime=end_time))
        return tx_receipt

    def offline_server(self, _user, _deviceId):
        tx_receipt = transaction(_user, self._contract.functions.offlineServer(_deviceId=_deviceId))
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

    def is_register(self, pub_key):
        pub_key = web3.Web3.to_checksum_address(pub_key)
        return self._contract.functions.isRegister(_user=pub_key).call()

    def get_account_info(self, pub_key):
        pub_key = web3.Web3.to_checksum_address(pub_key)
        try:
            address, balance, provider_blocked_funds, recipient_blocked_funds, info = self._contract.functions.getAccount(pub_key).call()
        except Exception as e:
            if not self.is_register(pub_key):
                raise Exception("please register first")
            raise e
        return UserInfo(address, balance, provider_blocked_funds, recipient_blocked_funds, info)

    def set_provider_info(self, addr, _info):
        tx_receipt = transaction(addr, self._contract.functions.setProviderInfo(_info))
        return tx_receipt

    def fuck_get(self, _deviceId):
        return self._contract.functions.getOfflineLeaseAndBilling(_deviceId=_deviceId).call()


contract_helper = HelperLib()


if __name__ == '__main__':
    print(HelperLib().register(role.provider))
    print(HelperLib().get_account_info(role.provider.public_key).info)
    import json
    print(HelperLib().set_provider_info(role.provider, json.dumps(dict(a=1, b=2))))
    print(HelperLib().get_account_info(role.provider.public_key).info)

    try:
        print(HelperLib().get_account_info(role.user.public_key).info) ## 测试一个不存在的key, 应该返回报错, 先注册
    except Exception as e:
        print(e)

    print(HelperLib().register(role.user))
    print(HelperLib().get_account_info(role.provider.public_key).info)

    # print("=" * 10, "测试质押", "=" * 10)
    # print(HelperLib().stake(role.provider, 13))
    # time.sleep(5)

    print("=" * 10, "上线机器", "=" * 10)
    print("online_server", HelperLib().online_server(role.provider, Machine(machine_id="ym-test", pub_key=role.provider.public_key, host="127.0.0.1", port="10", server_info=dict(a="a", b="b", c="c"), api_version="v0"), price=Price(server_price=10 ** 16, storage_price=10, upband_width=20, downband_width=30), start_time=int(time.time()), end_time=int(time.time()) + 10)['status'])

    # print(HelperLib().unstake(role.provider, 50))
    print("=" * 10, "test offline server", "=" * 10)
    print("list_devices", [(i.data['market_id'], i.data['status']) for i in HelperLib().list_devices(100, 0)])
    print("list_provider_lease", [i for i in HelperLib().list_provider_lease(role.provider.public_key, 1000, 0)])
    print("offline_server", HelperLib().offline_server(role.provider, 1)['status'])
    print("fuck_get", HelperLib().fuck_get(1))
    print([(i.data['market_id'], i.data['status']) for i in HelperLib().list_devices(100, 0)])
    # print([i.data['market_id'] for i in HelperLib().list_own_devices(role.provider, 10, 0)])
# 200000000000000000
# 100000000000000000
