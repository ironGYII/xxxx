# -*- coding:utf-8 -*-
import json
import os
import sys

url = 'http://6.tcp.cpolar.top:11150'
contract_address = '0x293b5e911A7b64D30240dd8afd3531345E1a9F2F'
gas_limit = 1000000  # 您可能需要根据合约函数的复杂性和资源消耗进行调整
chain_id = 1337

helper_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/Helper.json")))['abi']

public_to_private_keys = {
'0xB6D0b7dCbE45493c10b5f310aF116633857b5A07': '0xa80e7cee2bcdeb1203762a4450daf715485837776db5c01f0f12aba272deba6d',
'0xB089835CA456D8f0075a94F392CdAB2705FD2BAe': '0xb92f44f5cc70ed256a758fa94c652f96b3df70139db74e6aa1d3ddf6c4c63e85',
'0x9968430d5b46289A74Ba70A63997A054a9Aa6488': '0xdb537e37b859679fd570ad3a7ceb115bdbaff5899854adc43add39af007a8e85',
'0x72d382f5cDeBD13a0cBF14dccA20e41c6C5677c5': '0xa810a6d4a23352b7584fe7bfb650701f052f495773ef3dd6c4d77bcd8a66ef60',
'0x44B3b14C10055C42c529e5D07590E19E766F1f36': '0x1a0a6a5095e883115259a6c8b9fe8699a3999d34e4c40450f403aac169da84a7',
'0xC4E3bc8d8B50aa15dF267cd250a3f21d8C9b304d': '0xc2b9da22ee3bba516fc1167784364c8ca3e4451700d11f178af3bdda094ce072',
'0xF1AE70B240fAaE106c895dE897fABC27AaCA9448': '0x1a6ccf86ab6e8a6ff3d36995ef7504420612329d00a442a105696a73d6da627c',
'0x4e1Ef54E9317ff0eA849C2122E24cEd761b5eA65': '0xed2c4cc1ff30d5fb5cbd8f1fef548bdaa195bffda64f5974d5ab106ed291c4d5',
'0xd49Dcc1FEee013Eb9b7a595E7495a260A18a5C89': '0x82be4e2c7f44502765d67a268e2b2b70da6d62b4bfc8dd71a807b58b9610cafe',
'0x28C0B139D2C792C9d348FCA0eE8f852e1E1393D4': '0xd24490098cb565f908faf58c84d5a8f1b2b02ef3844f8520b86a90e2c2ead5d2'}



class _role:
    _contract_owner = '0xB6D0b7dCbE45493c10b5f310aF116633857b5A07'
    _provider = '0xB089835CA456D8f0075a94F392CdAB2705FD2BAe'
    _user = '0x9968430d5b46289A74Ba70A63997A054a9Aa6488'

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
