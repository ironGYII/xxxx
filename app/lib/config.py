# -*- coding:utf-8 -*-
import json
import os
import sys

# url = 'http://7.tcp.cpolar.top:11719'
# url = 'http://127.0.0.1:8545'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
account_contract_address = '0x7592A188A064395E54b2E7fE01b5C5554569D111'
account_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/AccountFactory.json")))['abi']

helper_contract_address = '0x976DE5a7aa0304D9F2F4a90De3A8c7C00629206b'
helper_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/Helper.json")))['abi']


gas_limit = 10000000 # 您可能需要根据合约函数的复杂性和资源消耗进行调整
# chain_id = 1337

url = 'https://linea-goerli.infura.io/v3/fedb760e61ff474e80caa22028b0348f'
chain_id = 59140

public_to_private_keys = {
'0xCAd129c097C6f496E1a89539427A1B4A727292C3': 'a3137bc8b100b6d707f16b0535ba3edde2a135ca502eb1eb8432e9ac377fab49',
# '0xdF31fd83C12BB3d66D07394A843E7b6065FcDaB0': '0x932ba50d15d7b02f9e6317bc56f88931c372553cfbc5da2ad68e1992f86ce7b4',
# '0x62DA151Df793d2E8eDB721BBa899FA55168A979A': '0x2bd1570a01dd4d8591822bd3b2f5832df1935aa6bbd1a6d3edf3c4abd77634df',
# '0xF458f69eC7C57be88c456eF2D492864dfC0Ca802': '0x148ca90033e7221081a6625dee17eb0e3b991bba1ef72c724ee219c5a7f17552',
'0x28E1E8fAE8dC002478394f8C7e2b2458E63D5605': 'ac0bf701d490ec0add953a0edb19b776739cc990ce07d334f15dfaa29e110e3b',
'0xB5B6ac8b55E03DA2440fE9803215b0A15cBcd9e3': '0xbc20ffa0e4b4ebcde1a4e5dd463837fefaf3387534ea486b4d7462f6339d00f6',
'0x17c66CD3A22287F12c8953cfe19F6Fe36f2d5d40': '0xb8782645368dc1cc70e7fa0a79a77ad95f8a226e75054de9fdd4b1a43fc5ac27',
'0xC73D43c392299866662f4BEd2c0e902a3A987647': '0x724d84ca0a09cff0444a55f271a846204095a53f4c78b8c2b3cfb5a4a9146921',
'0x3cb432EE97677f21e71C38A5E9c7d5BD528c9f32': '0x17ef0709c5be3977c573c44944c4a57486f1b28914762907b8514e656d6fb961',
'0x7929ee254982B00E0eAB67571a4058Ce16C0C6C8': '0x9804de8cf7f0e1b839c7522167decde90a254fa6f646373f978470e0b5ebb492'}


class _role:
    _contract_owner = '0xCAd129c097C6f496E1a89539427A1B4A727292C3'
    _provider = '0xCAd129c097C6f496E1a89539427A1B4A727292C3'
    _user = '0xCAd129c097C6f496E1a89539427A1B4A727292C3'

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
