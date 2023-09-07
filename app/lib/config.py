# -*- coding:utf-8 -*-
import json
import os
import sys

url = 'http://2.tcp.cpolar.top:13434'
url = 'http://127.0.0.1:8545'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
helper_contract_address = '0x0488395deC084042861AbcD77b154657b370a815'
helper_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/Helper.json")))['abi']

account_contract_address = '0xb030F0aB8fA5093f240423e301f981353Cf7Ee43'
account_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/AccountFactory.json")))['abi']

gas_limit = 1000000  # 您可能需要根据合约函数的复杂性和资源消耗进行调整
chain_id = 1337


public_to_private_keys = {
'0xB709ccf44a7fC374f3bFb4b637e74C551093d14b': '0x92726a12ebd2a4f7d5eab88a4b3742702f1e0f8886ccdb475c417ed823bc276b',
'0xA24d5b9CEFDe16cEfB488040B4f7de99e4dE92bB': '0xab62aa56a1a406115fac2b30c73f8225edbb0e8da908c554f3e64aa8163b1a9e',
'0xF4205a1102C7c760Fd003cdd8c517d7610905A49': '0xd42d254b2d90fe81fdb9b8880f51fb0255157546d41ddba53ef706b963c69823',
'0x6f750Fdbe7Dbb9FDf1F3aAABA3adBaCc8AdE3Ec1': '0x00830cc43d3424325711cd94025a53eacf635fab94492cb93d4e072a90fa0d57',
'0x1EaD778B949b60bfC5F132aF90fbC99d1f48c460': '0x86717ae32044e8260853cfd10e23ebd6147a75f9297e1e86329b335dc9ebe08d',  # 未注册用户
'0x7fe2CB205D853985C1b635A30429DA2977Bb06A0': '0x41589b31bfa89a88a28db254b3b38dd54bc55bbed067f69f9314514ea6ebba61',
'0x46016721a6C824F69eDab8Bf8c51Dd8C05a60468': '0x5c8011acdaa8fd22770688519f20138f63fe0800adbed3d4cad8e9a46da18f25',
'0xB589065B270E69078EBb09A6a63218F619e744fD': '0x005d43f40d16032865fc2783a1be2858da3aa5cc682326f620bb546413e4845b',
'0x1c414F0b2862ba3dEd759e21e2E8560410289Edf': '0x4434e759a8ff8764ef7e6ec66d2f70fec59f8da3f9b1305d802b6135c41aa0a0',
'0x9E40B1a5cB5b2c6D7217159070851317A93acb99': '0x19269b4cc021b21b1879ee8748bf3a0400ea5a0c603828c2a60301bd56eff791'}


class _role:
    _contract_owner = '0xB709ccf44a7fC374f3bFb4b637e74C551093d14b'
    _provider = '0xF4205a1102C7c760Fd003cdd8c517d7610905A49'
    _user = '0x6f750Fdbe7Dbb9FDf1F3aAABA3adBaCc8AdE3Ec1'

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
