import json
import random
import time

import web3

from scripts.config import role
from scripts.conn import market_contract, apus_iprover_contract, apus_token_contract,  apus_iprover_contract 


class ContractLib:
    # def online_server(self, _user, machine_info, price, start_time, end_time):
    #     tx_receipt = transaction(_user, self._helper_contract.functions.onlineServer(_machineId=machine_info.machine_id, _serverInfo=machine_info.contract_server_info, _price=price.contract_price, _startTime=start_time, _endTime=end_time))
    #     return tx_receipt

    def get(self):
        return market_contract.functions.get().call()





if __name__ == '__main__':
  contract_connector = ContractLib()
  contract_connector.get()