import json
from .config import role
from .conn import helper_contract, get_nonce, transaction


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

    def listDivices(self, _limit, _offset):
        pass

    def listOwnDevices(self, _provider, _limit, _offset):
        pass

    def listLease(self, _user, _limit, _offset):
        pass

    # 质押单位是ETH
    def stake(self, _user, amount):
        tx_receipt = transaction(_user, self._contract.functions.stake, value=int(amount * 10 ** 18))
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

    print(HelperLib().stake(role.provider, 33))