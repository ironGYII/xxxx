# -*- coding:utf-8 -*-
import json
import os
import sys

# url = 'http://7.tcp.cpolar.top:11719'
# url = 'http://127.0.0.1:8545'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
account_contract_address = '0x0511f0Cb37A57593741c42A88D4A3c14C389dF19'
account_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/AccountFactory.json")))['abi']

helper_contract_address = '0x8f1335A13A3f8D2c5989E14E76AC4a3F7b5B7F2f'
helper_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/Helper.json")))['abi']


gas_limit = 1000000  # 您可能需要根据合约函数的复杂性和资源消耗进行调整

url = 'https://rpc.jolnir.taiko.xyz'
chain_id = 167007

public_to_private_keys = {
'0xE8018D58e537aBa20cE5163ecb6171e179ab1636': 'a754ae659323d7bb824cf1188db0b3658c7f7a9fe01a76fdde829baa696a4f0e'
}


class _role:
    _contract_owner = '0xE8018D58e537aBa20cE5163ecb6171e179ab1636'
    _provider = '0xE8018D58e537aBa20cE5163ecb6171e179ab1636'
    _user = '0xE8018D58e537aBa20cE5163ecb6171e179ab1636'

    @classmethod
    def private_key(cls, public_key):
        return public_to_private_keys.get(public_key, None)

    @property
    def contract_owner(self):
        return type("owner", (), dict(public_key=self._contract_owner, private_key=self.private_key(self._contract_owner)))

    @property
    def provider(self):
        return type("provider", (), dict(public_key=self._provider, private_key=self.private_key(self._provider)))

    @property
    def user(self):
        return type("user", (), dict(public_key=self._user, private_key=self.private_key(self._user)))


role = _role()


__all__ = ['role', 'url', 'helper_contract_address', 'account_contract_address', 'helper_abi', 'account_abi', 'chain_id', 'gas_limit']

if __name__ == '__main__':
    print(role.provider.public_key)
    print(role.provider.private_key)
