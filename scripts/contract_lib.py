import json
import sys
import random
import time

import web3
import argparse
from scripts.config import role, env
from scripts.conn import *

none_address = '0x0000000000000000000000000000000000000000'

def gen_client_config(owner, client_id, url, max_instance, min_fee):
    return {
        'owner': owner,
        'id': client_id,  # 这是一个示例ID
        'url': url,  # 这是一个示例URL
        'minFee': min_fee,
        'maxZkEvmInstance': max_instance,
        'curInstance': 0,  # 这是一个示例的当前实例数
        'stat': 0
    }


class ContractLib:

    def join_market(self, prover, client_config):
        tx_hash = transaction(prover, market_contract.functions.joinMarket(client_config))
        return tx_hash

    def getLowestN(self):
        return market_contract.functions.getLowestN().call()

    def getProverConfig(self, addr, cid):
        return market_contract.functions.getProverConfig(addr, cid).call()

    def post_task(self, user, uniq_id):
        return transaction(user, apus_task_contract.functions.postTask(0, uniq_id, b"hello world! input", int(time.time()) + 90 * 60, dict(token=none_address, amount=10)))

    def dispatchTaskToClient(self, user, block_id):
        tx_hash2 = transaction(user, apus_task_contract.functions.dispatchTaskToClient(block_id))
        return tx_hash2

    def get_task(self, block_id):
        return apus_task_contract.functions.getTask(0, block_id).call()

    def get_task_by_index(self, index):
        return apus_task_contract.functions.tasks(index).call()

    def submit_task(self, user, task_id):
        tx_hash2 = transaction(user, apus_task_contract.functions.submitTask(0, task_id, b"8b6ffb96d2377872afd4998fb8329183abb8a321bde906059c8fa4643040728a"))
        return tx_hash2

    def market_dispatch(self, user, addr, cid):
        return transaction(user, market_contract.functions.dispatchTaskToClient(addr, cid))

    def has_resource(self):
        return apus_task_contract.functions.hasResource().call()



connector = ContractLib()


def creat_client_2():
    # provider 0xC2600C80Beb521CC4E2f1b40B9D169c46E391390
    client_config = gen_client_config(role.provider.public_key, 22, 'http://ec2-18-209-35-10.compute-1.amazonaws.com', 1, 10)

    print("-" * 10, "加入market client", "-" * 10)
    tx = connector.join_market(role.provider, client_config)
    print(tx['status'])

def create_client():
    # provider 0xC2600C80Beb521CC4E2f1b40B9D169c46E391390
    client_config = gen_client_config(role.provider.public_key, 11, 'http://3.235.67.158:9000', 1, 10)

    print("-" * 10, "加入market client", "-" * 10)
    tx = connector.join_market(role.provider, client_config)
    print(tx['status'])

    print("-" * 10, "获取价格最低client", "-" * 10)
    result = connector.getLowestN()
    print(result)


task_id = 1273181


def post_task():
    print("-" * 10, "推送task", "-" * 10)
    tx = connector.post_task(role.provider, task_id)
    print(tx['status'])


def get_task():
    print("-" * 10, "获取task & client", "-" * 10)
    result = connector.get_task(task_id)
    print(result)


def dispatch_task():
    print("-" * 10, "分配机器", "-" * 10)
    tx = connector.dispatchTaskToClient(role.provider, task_id)
    print(tx['status'])


def submit_task():
    print("-" * 10, "提交任务", "-" * 10)
    tx = connector.submit_task(role.provider, task_id)
    print(tx['status'])

def get_client_config():
    print("-" * 10, "获取client配置", "-" * 10)
    task, _ = connector.get_task(task_id)
    result = connector.getProverConfig(task[3], task[1])
    print(result)


def auto_init():
    client_config = gen_client_config(env['PROVER_PUBLIC_KEY'], int(env['CLIENT_ID']), env['CLIENT_URL'], int(env['MAX_ZKEVM_INSTANCE']), int(env['MIN_FEE']))
    print(client_config)
    print("-" * 10, "加入market client", "-" * 10)
    tx = connector.join_market(type("owner", (), dict(public_key=env['PROVER_PUBLIC_KEY'], private_key=env['PROVER_PRIVATE_KEY'])), client_config)
    if tx['status'] != 1:
        print("Join Market Failed")
    else:
        print("Join Market Success")


if __name__ == '__main__':
    # auto_init()
    # print(connector.market_dispatch(role.provider, '0x0000000000000000000000000000000000000000', 0)['status'])
    # create_client()
    # creat_client_2()
    # print(connector.market_dispatch(role.provider, '0xC2600C80Beb521CC4E2f1b40B9D169c46E391390', 170073054677)['status'])
    # print(connector.getLowestN())
    # print(connector.has_resource())
    # submit_task()
    # v = connector.get_task_by_index(43)
    # print(v)
    for index, i in enumerate(range(100000)):
        try:
            v = connector.get_task_by_index(i)
            print(index, ":", v[2], v[1], v[6])
        except:
            break
    # print(connector.getLowestN())
    # get_task()
    # dispatch_task()
    # get_task()
    # get_client_config()
    # submit_task()
    # get_task()
