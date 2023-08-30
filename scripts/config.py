# -*- coding:utf-8 -*-
import json

url = 'http://127.0.0.1:8545/'
contract_address = '0x1e83841d3DB52CCfd43094CF26d164A7fbe93346'
gas_limit = 1000000  # 您可能需要根据合约函数的复杂性和资源消耗进行调整
chain_id = 1337

helper_abi = json.load(open("build/contracts/Helper.json"))['abi']


public_to_private_keys = {
'0xfabF7764B4e3b08f629149cEA99Eeb85033edF21':'0x744ff21c7fb8e74f0df527758ed1c818dc86821195c1038a0d8bc877547630a7',
'0x7e2454BBe3F49851047f0fDc4e178296431e5494':'0x70a22ea91fc82fb61bed7840142be24a0b558b9f188196b6a152c10acbbba83f',
'0x86f41E73c8bE844A7Cd267Fff270a6A7C5469A09':'0xc45423ae652662f4fb520cbdc76fd4e12966c56982be3c1d28e5c03b4c523f45',
'0xbBE040F3aF147bD35cbe70f8aDF1fCf79828dE6b':'0x032dff5f54594b944202cb2e56d0d0038f414cb6bb08de54c7f5b21ca3665f7a',
'0xBa5f26D6996015A14AF19F87C97c6eB5FA3B0992':'0xaeddbd9ef46afee13cad4196eaf31bc33584cbfc67d895d3defe1409ebdc1429',
'0x4fDA00e4CF61b26CBa0c621CdA25e9Be210fA6ea':'0xe0f9d41bb2997a0bb79e3318680365f5e49976b86628f47bdd320e1d3c22217c',
'0x104BdD33415A3Def91db03776c03528de4Ad5187':'0xa500c11167a62cdf42ae7852b8418666bb210099be676a00e44e5ab2815d6367',
'0x4Aa43D8df9C1aAC0e5E5c67fcf099fC2183d7046':'0xb51f1efdca615a963eb7df208b0c788db41e0612bac869d720d284d07831a1f0',
'0x613feF1aCd181CDbC8F2E307Fdb0b3F593dADab7':'0x018b78231e65e88eecb4b1658e2b50081b36a26cbbf6e645bbe939bcb7a4176e',
'0x91591ED9d98D673CA7351aB68cb7F1460d796C10':'0x4bab744e88df6b97616c0eaf5f413152ebdb09cadc4738a52c87026f225382f0'}

class _role:
    _contract_owner = '0xfabF7764B4e3b08f629149cEA99Eeb85033edF21'
    _provider = '0x7e2454BBe3F49851047f0fDc4e178296431e5494'
    _user = '0x86f41E73c8bE844A7Cd267Fff270a6A7C5469A09'

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



__all__ = ['role', 'url', 'contract_address', 'helper_abi', 'chain_id', 'gas_limit']

if __name__ == '__main__':
    print(role.provider.public_key)
    print(role.provider.private_key)
