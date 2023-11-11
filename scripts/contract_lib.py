import json
import random
import time

import web3
import argparse
from scripts.config import role
from scripts.conn import *

none_address = '0x0000000000000000000000000000000000000000'

def gen_client_config(owner, url, max_instance, min_fee):
    client_id = int(time.time() * 100)
    return {
        'owner': owner.public_key,
        'id': client_id,  # 这是一个示例ID
        'url': url,  # 这是一个示例URL
        'minFee': min_fee,
        'maxZkEvmInstance': max_instance,
        'curInstance': 0  # 这是一个示例的当前实例数
    }


class ContractLib:

    def join_market(self, prover, client_config):
        tx_hash = transaction(prover, market_contract.functions.joinMarket(client_config))
        return tx_hash

    def getLowestN(self):
        return market_contract.functions.getLowestN().call()

    def getProverConfig(self, cid):
        return market_contract.functions.getProverConfig(role.contract_owner.public_key, cid).call()

    def post_task(self, user, uniq_id):
        return transaction(user, apus_task_contract.functions.postTask(0, uniq_id, b"hello world! input", int(time.time()) + 90 * 60, dict(token=none_address, amount=10)))

    def dispatchTaskToClient(self, user, cid, taskID):
        tx_hash2 = transaction(user, apus_task_contract.functions.dispatchTaskToClient(user.public_key, cid, taskID))
        return tx_hash2

    def get_task(self, index):
        return apus_task_contract.functions.tasks(index).call()

    def submit_task(self, user, task_id):
        tx_hash2 = transaction(user, apus_task_contract.functions.submitTask(task_id, b"result"))
        return tx_hash2


if __name__ == '__main__':
    # 新增一个client
    connector = ContractLib()
    task_id = 3
    task_uniq_id = int(time.time())
    client_config = gen_client_config(role.provider, 'http://' + str(int(time.time())) + '.com', 1, 10)
    print("-" * 10, "加入market client", "-" * 10)
    tx = connector.join_market(role.provider, client_config)
    print(tx['status'])

    print("-" * 10, "获取价格最低client", "-" * 10)
    result = connector.getLowestN()
    print(result)

    print("-" * 10, "prover client 信息", "-" * 10)
    result = connector.getProverConfig(client_config['id'])
    print(result)

    print("-" * 10, "post task", "-" * 10)
    tx = connector.post_task(role.provider, task_uniq_id)
    print(tx['status'])

    print("-" * 10, "get task", "-" * 10)
    result = connector.get_task(task_id - 1)
    print(result)

    print("-" * 10, "dispatchTaskToClient", "-" * 10)
    print("pre: state", connector.getProverConfig(client_config['id']))
    tx = connector.dispatchTaskToClient(role.provider, client_config['id'], task_id)
    print("end: state", tx['status'], connector.getProverConfig(client_config['id']), connector.get_task(task_id - 1))

    print("-" * 10, "submit task", "-" * 10)
    tx = connector.submit_task(role.provider, task_id)
    print("end: state", tx['status'], connector.getProverConfig(client_config['id']), connector.get_task(task_id - 1))
