# -*- coding:utf-8 -*-
import json
import os
import sys

url = 'http://2.tcp.cpolar.top:13434'
url = 'http://127.0.0.1:8545'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
# contract_address = '0xBfFd481336eac92e381D990636d9e8be7e909bFd'
helper_contract_address = '0x3A65726e24b00860C51222a7E4a7e303c5C0E834'
helper_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/Helper.json")))['abi']

account_contract_address = '0x69dA56a347acBc6Cae2464dD6943fd1774F2fD61'
account_abi = json.load(open(os.path.join(os.getcwd(), "build/contracts/AccountFactory.json")))['abi']

gas_limit = 1000000  # 您可能需要根据合约函数的复杂性和资源消耗进行调整
chain_id = 1337


public_to_private_keys = {
'0x1a8E1BEBd5abc6E6ADc3dAC3aa73243fAEab64A7': '0xcb2c768529226aafee79fd9e74cf2d2f3e0c4136bfc00c3ffd68e7c62ecfc7b3',
'0x0dE70097283EAac8cf0F5304Ed69476A6Bf6af4E': '0xb7b0634364ecc2ade8709f6466209b48a74480e7ee45e7503c8af0bb38590a9d',
'0x4511aA6140EaD2A2696007E0235612913dA79a11': '0x26af05a026706fde3d52cbf009cc011066077166705f09c6045b995763e75fb0',
'0x896dEC362445F4b67AB7ED675c810e16d85C365c': '0xf782aa4fd090cb3c1e66d6186b7bad91f398a5c0b9631d45b7811323a7f85890',
'0x7dDEC97027d2935dE14Be602969A07443B003fF9': '0xd6bb87bbf59582424eac39b4c013767ba386425bd94d7330d369b24ba35db22e',
'0x99Ca0f373c7925171a8B6201b7afa7fc474dC63b': '0x7456c1dcc9cbf5321da072e4d8d4c0904df4126cda62c1711b437297da1ad232',
'0xf2abcb4B4e18356F66fD96f7B6522c5D528AFA52': '0x8ca9f54c05602366971c8e8eb4fcab86db4f1c5e26a73548a924d49bb4713951',
'0x629b96BeceaFF92e2537A6205Cb7F05D08D2dd0e': '0x4cdb9d6170babd19aa0beeff95ac3a9ad68b62434493bf8fc986689946535524',
'0x2d8d84Fe38Bc6C5e749c1fF37560574Fd43BD10c': '0x3a3c956b38313f8cd437ae7078033aed2b28ccf77cc77683478957c936d8fbff',
'0x51e798442B19bB2b05Ba5235D3A9DA6b0A0b2a07': '0xf184fcd8e4610671542e1ce805c0745cfd2e5f08092ced8d4a98a9590d917fad'}


class _role:
    _contract_owner = '0x1a8E1BEBd5abc6E6ADc3dAC3aa73243fAEab64A7'
    _provider = '0x7dDEC97027d2935dE14Be602969A07443B003fF9'
    _user = '0x99Ca0f373c7925171a8B6201b7afa7fc474dC63b'

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
