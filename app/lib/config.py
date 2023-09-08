# -*- coding:utf-8 -*-
import json
import os
import sys

url = 'http://9.tcp.cpolar.top:11292'
url = 'http://127.0.0.1:8545'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
account_contract_address = '0xD5c06d5B4b9c1A9E3Ec1ADb893514F2fe039d6e3'
account_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/AccountFactory.json")))['abi']

helper_contract_address = '0x5CF121027c5338aB310f7A09c4B6ed22Ad3bDD0A'
helper_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/Helper.json")))['abi']


gas_limit = 1000000  # 您可能需要根据合约函数的复杂性和资源消耗进行调整
chain_id = 1337


public_to_private_keys = {
'0x8f7C4591922c97885598941D63a0D2CB070C3edd': '0xc7b52a1420295a999ec0f394709268dad5c7f3bf994a4eb6aa6cf6ef9edc8283',
'0x2508Fa7A678615B8385c6701d7017081aC62ff9C': '0x36dbd8cb4ddea7e266f18ef5bd6dc42755a9f880c38c1fbe20c3fa8239c752e2',
'0xC99b11BF91a11d732Da63dC1A4B6684E62BA9857': '0xe2d734f0b982ebc834013015315f1a2541c11588952d705e7cec9ff03a9f108d',
'0x06cB2c2f87B4e56e0e9330a3dF35c2b27c817F05': '0x5ce1a4e841c15f03d5d67b404d6626d8e6364a859b17371f0770f4f31f1d8cd8',
'0x030b281C45c6371880f04D73450486b1ec712421': '0xb475f5dd2747f79af9dd14c16a4310bf4dff9212051da5d19c69f03c09c883ed',
'0xca694aB58298fb2D707A1a53106F5C4eA52DD62C': '0x4d0b040513ca92435c76f19272105b597e952feb2f77ec964e193ff92620542c',
'0x927eF1A025Ef203287ABFb440eD006C06C576EDC': '0x8e7ede427f341b5f6a570c86960ee379dd2dac43f3005686efabe5c9c14dac9e',
'0x3F82e9757a04B1Bfd29536319A497d49A5894555': '0x7f29d030ecbd197df585c5eafbe2446b96d9f365e511495bcfd750cec2b2ff32',
'0xb733a7f772429EEbBC854D64d7b525A3941667f1': '0x6289e71fd08a61d9b6c61992a7e0bf4f8882e805dda0adbfd77cfdb8d4423c04',
'0xe20A554746ecE1FDb3F90B4bF76fE7eB065675fD': '0x5296560a9da9cf72344a1e7bca66e00a308228ff35d240ab746c55145961f9a2'}

class _role:
    _contract_owner = '0x8f7C4591922c97885598941D63a0D2CB070C3edd'
    _provider = '0x927eF1A025Ef203287ABFb440eD006C06C576EDC'
    _user = '0xC99b11BF91a11d732Da63dC1A4B6684E62BA9857'

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
