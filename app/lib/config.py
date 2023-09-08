# -*- coding:utf-8 -*-
import json
import os
import sys

url = 'http://2.tcp.cpolar.top:15121'
url = 'http://127.0.0.1:8545'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
helper_contract_address = '0x00fea3E5653870341DE95F9d3f202b0a2D2B0fc5'
helper_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/Helper.json")))['abi']

account_contract_address = '0xb73D7Db6d5D46c125C8c542e0e2F95114d46a9e0'
account_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/AccountFactory.json")))['abi']

gas_limit = 1000000  # 您可能需要根据合约函数的复杂性和资源消耗进行调整
chain_id = 1337


public_to_private_keys = {
'0x35f425f9e97ee5E6ff52E8898c7682f9823737a6': '0xb72a906b076d66f350af79cab7645b9d3b9525cf3decdfd4f665b54afc1518e1',
'0xFD5D4AF80B1d277d29a905a359d95932B174B70F': '0x12dab77ed9cf096ae8389db1b381cb7c23a3d7f63c4f2a33e08d1fa3b0fa5692',
'0x86f0A52AAEf587989bacEf567fB17E915055e4dF': '0xf847182263a1282e7ca5ed7ec1b6e9f872137a8b6138fefd6ecee162603ff56d',
'0x31209D978183b7ee91f5B96D4f200e4fc1D279dB': '0x8bb9dd43ad186858ab8df2eb836c4f88b85593bcc014d67e0f84694abee1ac8e',
'0x6b005C55659409CeD0F24dA43de0082b81371942': '0x61ab9de1754185d92283de3b82d1ecd24bc45fb39a08f5f7cbb9ddd929e8ef29',
'0x1Fd8fD4619b90c9805E739AE200A56f2e82e88ca': '0x5346f33b34d934fecfb908c76f07599b6f7648cc33a449bc3b39a31e6c2e5d14',
'0x24C4439f7DF053029EcC4a1B2cC096C090e51a21': '0x0fb6818e3738db7abcfc984c29cef79d2371a8d3ac22225eda4548e7dc837868',
'0x60a6A97D3d09459023DCC53664B0a6dd3db90290': '0x17872f7d638ef291a8f7be3e35e295ccf4f99670290f00f184bacceb2a95d91d',
'0xfDFf0070b7691FdeBeDeB79c7B3F860cA8181cF5': '0xdc7b72653dfbd88427c9c6216c432ae41798f9f778374b049ec89b6bfa882ddf',
'0x66Ee06246a3d77227F9f3Af116404C5B4B293785': '0x4ef14593e29f95a6986e54b3c4778bf4bfaa542d02a5c18e80306383b8fb0f96'}


class _role:
    _contract_owner = '0x35f425f9e97ee5E6ff52E8898c7682f9823737a6'
    _provider = '0xFD5D4AF80B1d277d29a905a359d95932B174B70F'
    _user = '0x86f0A52AAEf587989bacEf567fB17E915055e4dF'

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
