import json
import random
import time

import web3
import argparse
from scripts.config import role
from scripts.conn import market_contract, apus_iprover_contract, apus_token_contract,  apus_iprover_contract, transaction, market_contract_address, web3

from eth_keys import keys

# 以太坊私钥
def get_pub_key(pk):
    account = web3.eth.account.from_key(pk)
    # # 从私钥创建一个以太坊密钥对象
    # private_key = keys.PrivateKey.from_hex(pk)

    # # 获取公钥
    # public_key = private_key.public_key

    # # 获取以太坊公钥地址
    # public_key_hex = public_key.to_hex()
    # public_key_address = public_key.to_checksum_address()

    # # 打印公钥和地址
    # print("公钥 (hex):", public_key_hex)
    # print("地址:", public_key_address)
    return account.address

def gen_client_config(owner, url, max_instance, min_fee):

    client_id = int(time.time() * 100)
    return {
        'owner': owner,
        'id': client_id,  # 这是一个示例ID
        'url': url,  # 这是一个示例URL
        'minFee': min_fee,
        'maxZkEvmInstance': max_instance,
        'curInstance': 0  # 这是一个示例的当前实例数
    }


class ContractLib:
    # def online_server(self, _user, machine_info, price, start_time, end_time):
    #     tx_receipt = transaction(_user, self._helper_contract.functions.onlineServer(_machineId=machine_info.machine_id, _serverInfo=machine_info.contract_server_info, _price=price.contract_price, _startTime=start_time, _endTime=end_time))
    #     return tx_receipt

    def get(self):
      return market_contract.functions.get().call()

    def set_address(self):
      print(transaction(role.provider, apus_iprover_contract.functions.setProofTaskContract(role.contract_owner.public_key)))

    def join_market(self, prover, client_config):
        # 这里假设client_config是一个字典，它的键对应ApusData.ClientConfig结构体的字段
        tx_hash = transaction(
            prover, market_contract.functions.joinMarket(client_config))
        # 返回交易哈希，以便稍后可以查看交易状态或收据
        return tx_hash

    def getLowestN(self):
        return market_contract.functions.getLowestN().call()

    def getProverConfig(self, cid):
        return market_contract.functions.getProverConfig(role.contract_owner.public_key, cid).call()

    def dispatchTaskToClient(self, cid):
         tx_hash2 = transaction(role.contract_owner, market_contract.functions.dispatchTaskToClient(role.contract_owner.public_key, cid))
         return tx_hash2
    
    def releaseTaskToClient(self, cid):
        tx_hash2 = transaction(role.contract_owner, market_contract.functions.releaseTaskToClient(role.contract_owner.public_key, cid))
        return tx_hash2

    def task_dispatchTaskToClient(self):
         tx_hash2 = transaction(role.contract_owner, apus_token_contract.functions.dispatchTaskToClient(role.contract_owner.public_key, client_id))
         return tx_hash2
    
    def task_releaseTaskToClient(self):
        tx_hash2 = transaction(role.contract_owner, apus_token_contract.functions.releaseTaskToClient(role.contract_owner.public_key, client_id))
        return tx_hash2

    def task_set_market_address(self):
        tx_hash2 = transaction(role.contract_owner, apus_token_contract.functions.setMarket(market_contract_address))
        return tx_hash2



if __name__ == '__main__':
    contract_connector = ContractLib()
    # print(contract_connector.get())


    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='apus taiko client')
    parser.add_argument('private_key', type=str, help='prover private key')
    parser.add_argument('url', type=str, help='URL for prover client')
    parser.add_argument('max_instance', type=int, help='max proof task instance')
    parser.add_argument('min_fee', type=int, help='max proof task instance')
    args = parser.parse_args()

    prover = type("prover", (), dict(public_key=get_pub_key(args.private_key), private_key=args.private_key))
# def gen_client_config(owner, url, max_instance, min_fee):
    print(gen_client_config(prover.public_key, args.url, args.max_instance, args.min_fee))

    tx_hash = contract_connector.join_market(prover, gen_client_config(prover.public_key, args.url, args.max_instance, args.min_fee))

    # # print(f"Sent joinMarket transaction with hash: {tx_hash}")

    # # def gen_client_config(owner, url, max_instance, min_fee):

    for i in range(10):
        gln = contract_connector.getLowestN()
        print(f"\n LowestN:{gln[1][1]}")

        print(f"\n get Prover:{contract_connector.getProverConfig(gln[1][1])}")

        break
        # contract_connector.dispatchTaskToClient(gln[1][1])

    # tx_hash1 = contract_connector.task_set_market_address()
    # print(f"\n get Prover:{contract_connector.getProverConfig()}")

    # print("FUCKKKKKKKKKKK")
    # tx_hash1 = contract_connector.task_dispatchTaskToClient()
    # print(f"\n Sent dispatchTaskToClient transaction with hash: {tx_hash1}")
    # print(f"\n get Prover:{contract_connector.getProverConfig()}")

    # tx_hash2 = contract_connector.task_releaseTaskToClient()
    # print(f"\n Sent releaseTaskToClient transaction with hash: {tx_hash2}")
    # print(f"\n get Prover:{contract_connector.getProverConfig()}")

