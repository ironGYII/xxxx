from conn import helper_contract, get_nonce, transaction
from config import role


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

    # 质押单位是wei
    def stake(self, _user, amount):
        stake

    def register(self, addr):
        tx_receipt = transaction(addr, self._contract.functions.register())
        return tx_receipt

    def get_account_info(self, addr):
        account_info = self._contract.functions.getAccount(addr.public_key).call()
        return account_info

    def set_provider_info(self, addr, _info):
        tx_receipt = transaction(addr, self._contract.functions.setProviderInfo(_info))
        return tx_receipt


if __name__ == '__main__':
    print(HelperLib().register(role.provider))
    print(HelperLib().get_account_info(role.provider))
    import json
    print(HelperLib().set_provider_info(role.provider, json.dumps(dict(a=1, b=2))))
    print(HelperLib().get_account_info(role.provider))