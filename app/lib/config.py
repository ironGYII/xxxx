# -*- coding:utf-8 -*-
import json
import os
import sys

url = 'http://9.tcp.cpolar.top:10861'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
account_contract_address = '0x36A4D97E5cfb4D7116432EBD2ff3C175599D0fCe'
account_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/AccountFactory.json")))['abi']

helper_contract_address = '0xCB875Ce36AcE8878B74aB6af90D24EcC57491E29'
helper_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/Helper.json")))['abi']


gas_limit = 1000000  # 您可能需要根据合约函数的复杂性和资源消耗进行调整
chain_id = 1337


public_to_private_keys = {
'0x51ABBC385AE0bD3c9247B999dc1c2146Fb6F2429': '0x78f28c9dd9a5251ca0f9afbaa2a9869996afb1b63cbc974685205c7ed307e57e',
'0x81eCb14C77a8Fcc59040eDf6fab96F9Aa25cC6B8': '0x2abd656d876ca56e3ce9b71fad5344a38c55f46ce7d4297bc21e79167b0d075e',
'0x56e48deBc4aff73d3fc226A9E71339b0fb44BDbb': '0xcad798b4b670c65d29b1cdb1e89380fce01ebb0521b78356cf60b1bb412ecdbe',
'0xaa6874eF9DB03b46BBd109DBA9da4B381E2Bb1AD': '0xf797724af80712ae67d2e4c3472f15f3e4409ebf6aee98cc11023b22425d9862',
'0x5942e7a28035c0154F2f9b1610CCe1D2E1F5D172': '0xd476f6cf3bbbc0d13fc6dced78a607a2dc39f77e6914a3438e44a1427b4b7d29',
'0xa1DBc763379e067b13fB444320Edf8521C94f423': '0xc97b0afe49279c0c9a15be6f7111a271d5d11fa54deeab2bcc31ebde14724b75',
'0xCc84d0a4870177531195043bde99B38EB56132b3': '0xbed48bcd667635406eface910da6b0445c0e4661b559a1c7057cfa906d8815f7',
'0xB578D77875751EC84b6F2c22EF3c59086875db30': '0x1417acfc3c7f893e195d1c70db0549a7986d25fece3edf36560bfc6f918e9f7b',
'0xB6f1e22d0788f2c48C443cd9965F6C3Ee43b6620': '0xac247b2559a58f80c8a069a920e586223f8d8fa4be462febc435c7c973391ce7',
'0x375958BFfEFe8df7FB6B829222C25c0c031C59C7': '0x75655f02cf2ecd5d129a57654ead739f57bd3bdcb740b50456e473868dc34d06'}

class _role:
    _contract_owner = '0x51ABBC385AE0bD3c9247B999dc1c2146Fb6F2429'
    _provider = '0x81eCb14C77a8Fcc59040eDf6fab96F9Aa25cC6B8'
    _user = '0x56e48deBc4aff73d3fc226A9E71339b0fb44BDbb'

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
