# -*- coding:utf-8 -*-
import json
import os
import sys

# Localhost
url = 'http://1.117.58.173:8545'
chain_id = 1337
gas_limit = 1000000  # 您可能需要根据合约函数的复杂性和资源消耗进行调整

public_to_private_keys = {
    '0xC2600C80Beb521CC4E2f1b40B9D169c46E391390' :'0x91c6c377cc072cd187fed1caaa6527896f58f10cb20667235c87b07c64b33955'
}

# Sepolia
# url = 'https://eth-sepolia.g.alchemy.com/v2/j1yrdLvznv5AQ5NfphKOQZsFDU7-Jc8W'
# chain_id = 11155111
# public_to_private_keys = {
#     '0x122b93Ff43d17D6f8D93fB1dEa6faDac20489fA9' :'88d57d52b4eedc76ca40bd52bc36c16795d61972ec8ff530ad74dc9bcd17299a'
# }


class _role:
    _contract_owner = '0xC2600C80Beb521CC4E2f1b40B9D169c46E391390'
    _provider = '0xC2600C80Beb521CC4E2f1b40B9D169c46E391390'
    _user = '0xC2600C80Beb521CC4E2f1b40B9D169c46E391390'

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


def get_config(fileName):
    return json.load(open(os.path.join(os.getcwd(), "build/contract_address", fileName)))['address'], json.load(open(os.path.join(os.getcwd(), "build/contracts", fileName)))['abi']

market_contract_address, market_abi = get_config("Market.json")
apus_task_address, apus_task_abi = get_config('ApusProofTask.json')

__all__ = ['role', 'url', 'chain_id', 'gas_limit', 'market_contract_address', 'market_abi', 'apus_task_address', 'apus_task_abi']

if __name__ == '__main__':
    print(role.provider.public_key)
    print(role.provider.private_key)
