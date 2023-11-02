import json
import random
import time

import web3

from scripts.config import role
from scripts.conn import market_contract, apus_iprover_contract, apus_token_contract,  apus_iprover_contract, transaction


class ContractLib:
    # def online_server(self, _user, machine_info, price, start_time, end_time):
    #     tx_receipt = transaction(_user, self._helper_contract.functions.onlineServer(_machineId=machine_info.machine_id, _serverInfo=machine_info.contract_server_info, _price=price.contract_price, _startTime=start_time, _endTime=end_time))
    #     return tx_receipt

    def get(self):
        return market_contract.functions.get().call()

    def join_market(self, client_config):
        # 这里假设client_config是一个字典，它的键对应ApusData.ClientConfig结构体的字段
        tx_hash = transaction(
            role.provider, market_contract.functions.joinMarket(client_config))
        # 返回交易哈希，以便稍后可以查看交易状态或收据
        return tx_hash

    def getLowestN(self):
        return market_contract.functions.getLowestN().call()

    def getProverConfig(self):
        return market_contract.functions.getProverConfig("0x1234567890123456789012345678901234567890", 1).call()

    def dispatchTaskToClient(self):
         tx_hash2 = transaction(role.provider, market_contract.functions.dispatchTaskToClient("0x1234567890123456789012345678901234567890", 1))
         return tx_hash2
    
    def releaseTaskToClient(self):
        tx_hash2 = transaction(role.provider, market_contract.functions.releaseTaskToClient("0x1234567890123456789012345678901234567890", 1))
        return tx_hash2


if __name__ == '__main__':
    contract_connector = ContractLib()
    print(contract_connector.get())

client_config = {
    'owner': '0x1234567890123456789012345678901234567890',  # 使用一个有效的Ethereum地址替换此处的占位符
    'id': 1,  # 这是一个示例ID
    'url': 'http://example.com',  # 这是一个示例URL
    'minFee': 100,  # 这是一个示例费用，可以根据需要更改
    'maxZkEvmInstance': 5,  # 这是一个示例的最大实例数
    'curInstance': 2  # 这是一个示例的当前实例数
}

tx_hash = contract_connector.join_market(client_config)

print(f"Sent joinMarket transaction with hash: {tx_hash}")

print(f"\n LowestN:{contract_connector.getLowestN()}")

print(f"\n get Prover:{contract_connector.getProverConfig()}")

tx_hash1 = contract_connector.dispatchTaskToClient()
print(f"\n Sent dispatchTaskToClient transaction with hash: {tx_hash1}")

tx_hash2 = contract_connector.releaseTaskToClient()
print(f"\n Sent releaseTaskToClient transaction with hash: {tx_hash2}")