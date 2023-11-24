
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// import "./console.sol";
import "./ApusData.sol";


contract Market {
    // Search the n'st lowest price prover 

    ApusData.ClientConfig [] public clients;


    // function get() public view returns(uint256){
    //     uint256 count = 5;
    //     // console.log('count: %d', count);
    //     // console.log();
    //     return count;
    // }

    function setTask(address _as)  public {
    }

    function joinMarket(ApusData.ClientConfig memory cf) public {

        for (uint i = 0; i < clients.length; i++) {
            if (clients[i].owner == cf.owner && clients[i].id == cf.id) {
                if (clients[i].stat != ApusData.ClientStatus.Stopped) {
                    revert("client already running");
                }
                clients[i].stat = ApusData.ClientStatus.Running;  // Releasing a task from the client
                return ;
            }
        }
        cf.stat = ApusData.ClientStatus.Running;
        clients.push(cf);
        // console.log("market j");
    }

    //获取价格最低的N台机器。当前版本直接固定N == 1 会简化很多。
   function getLowestN() public view returns(address owner, ApusData.ClientConfig memory cf) {
       uint256 lowestFee = type(uint256).max;  // 初始化为uint256的最大值
       ApusData.ClientConfig memory cheapestClient;

       // 遍历每一个客户端
       for(uint i = 0; i < clients.length; i++) {
           if(clients[i].curInstance < clients[i].maxZkEvmInstance   && clients[i].minFee <= lowestFee && clients[i].stat == ApusData.ClientStatus.Running) {
               lowestFee = clients[i].minFee;
               cheapestClient = clients[i];
           }
       }

       // 确保我们至少找到一个在线的机器
       require(cheapestClient.curInstance < cheapestClient.maxZkEvmInstance, "No online clients found");
       return (cheapestClient.owner, cheapestClient);
   }

   function getProverConfig(address owner, uint256 clientID) public view returns (ApusData.ClientConfig memory cf){
       ApusData.ClientConfig memory clientConfig;
   
       // console.log('client count: %d', clients.length);
       // console.log('client parameter count: %x', owner);
       // console.log('clients[0] adress:: %x', clients[0].owner);
           // 遍历每一个客户端
       for(uint i = 0; i < clients.length; i++) {
           if(clients[i].owner == owner  && clients[i].id == clientID) {
               clientConfig = clients[i];
               break;
           }
       }
   
       require(bytes(clientConfig.url).length > 0, "No online clients found");
       return(clientConfig);
   }

   function dispatchTaskToClient(address owner, uint256 clientID) public returns (bool success) {
        for (uint i = 0; i < clients.length; i++) {
            if (clients[i].owner == owner && clients[i].id == clientID) {
                if (clients[i].curInstance < clients[i].maxZkEvmInstance) {
                    clients[i].curInstance += 1;  // Assigning a task to the client
                    return true;
                }
                return false;  // The client can't take more tasks
            }
        }
        revert("Client not found");
    }

    function releaseTaskToClient(address owner, uint256 clientID) public returns (bool) {
        for (uint i = 0; i < clients.length; i++) {
            if (clients[i].owner == owner && clients[i].id == clientID) {
                require(clients[i].curInstance > 0, "No tasks to release for this client");
                clients[i].curInstance -= 1;  // Releasing a task from the client
                return true;
            }
        }
        revert("Client not found");
    }

    function offlineClient(address owner, uint256 clientID) public {
        for (uint i = 0; i < clients.length; i++) {
            if (clients[i].owner == owner && clients[i].id == clientID) {
                clients[i].stat = ApusData.ClientStatus.Stopped;
                return ;
            }
        }
        revert("Client not found");
    }

    function marketCapacity() public view returns(uint256) {
        uint256 capacity = 0;
        for (uint i = 0; i < clients.length; i++) {
            if (clients[i].stat == ApusData.ClientStatus.Running) {
                capacity += clients[i].maxZkEvmInstance - clients[i].curInstance;
            }
        }
        return capacity;
    }
}