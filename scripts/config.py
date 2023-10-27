# -*- coding:utf-8 -*-
import json
import os
import sys

url = 'http://1.117.58.173:8545'
chain_id = 1337
gas_limit = 1000000  # 您可能需要根据合约函数的复杂性和资源消耗进行调整

public_to_private_keys = {
    '0x2b916e0d058201Ab046f673b7D42a279ADd78B7B': '0x94baf6ab65a09759a30d1803cee7356c2f8fef2a3e8aab7e2f442736f4b24a2d'
}

class _role:
    _contract_owner = '0x2b916e0d058201Ab046f673b7D42a279ADd78B7B'
    _provider = '0x2b916e0d058201Ab046f673b7D42a279ADd78B7B'
    _user = '0x2b916e0d058201Ab046f673b7D42a279ADd78B7B'

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

market_contract_address, market_abi = get_config('Market.json')
apus_token_contract_address, apus_token_abi = get_config('ApusToken.json')
apus_iprover_contract_address, apus_iprover_abi = get_config('ApusIProver.json')
binding_contract_address, binding_abi = get_config('Binding.json')
# print(market_contract_address)
# print(apus_token_contract_address)
# print(apus_iprover_contract_address)
# print(binding_contract_address)

__all__ = ['role', 'url', 'chain_id', 'gas_limit', 'market_contract_address', 'market_abi', 'apus_token_contract_address', 'apus_token_abi', 'apus_iprover_contract_address', 'apus_iprover_abi', 'binding_contract_address', 'binding_abi']

if __name__ == '__main__':
    print(role.provider.public_key)
    print(role.provider.private_key)
