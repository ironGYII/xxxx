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

    def set_address(self):
      print(transaction(role.provider, apus_iprover_contract.functions.setProofTaskContract("0xe9B85f5413D0a6783b96CFE014D3d2A1F179b0cA")))



if __name__ == '__main__':
  contract_connector = ContractLib()
  print(contract_connector.get())
  print(contract_connector.set_address())