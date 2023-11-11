
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./market.sol";
import "./token.sol";

import "./ApusData.sol";

contract ApusProofTask {

    ApusData.Task [] public tasks;

    Market private market;
    ERC20 private token;

    event eventPostTask(uint256 taskId, uint256 fee, address tokenAddress);

    constructor(address _marketAddr, address _tokenAddr) {
        market = Market(_marketAddr);
        token = ERC20(_tokenAddr);
    }

    function submitTask(ApusData.TaskType _tp, uint256 uniqID, bytes calldata result) public {
        for (uint256 i = 0; i < tasks.length; i++) {
            if (tasks[i]._tp ==  _tp && tasks[i].uniqID == uniqID) {
                require(tasks[i]._stat == ApusData.TaskStatus.Assigned);
                tasks[i]._stat = ApusData.TaskStatus.Done;
                tasks[i].result = result;
                market.getProverConfig(tasks[i].assigner, tasks[i].clientId);
                market.releaseTaskToClient(tasks[i].assigner, tasks[i].clientId);
                token.reward(tasks[i].assigner);
                return ;
            }
        }

    }

    function getTask(ApusData.TaskType _tp, uint256 uniqID) public view returns(ApusData.Task memory, ApusData.ClientConfig memory){
        for (uint256 i = 0; i < tasks.length; i++) {
            if (tasks[i]._tp ==  _tp && tasks[i].uniqID == uniqID) {
                if (tasks[i]._stat != ApusData.TaskStatus.Posted) {
                    ApusData.ClientConfig memory cf = market.getProverConfig(tasks[i].assigner, tasks[i].clientId);
                    return (tasks[i], cf);
                }
                return (tasks[i], ApusData.ClientConfig(address(0), 0, "", 0, 0, 0));
            }
        }
        revert("unknow task");
    }

    function postTask(ApusData.TaskType _tp, uint256 uniqID, bytes calldata input, uint64 expiry, ApusData.rewardInfo memory ri) public {
        for (uint256 i = 0; i < tasks.length; i++) {
            if (tasks[i]._tp ==  _tp && tasks[i].uniqID == uniqID) {
                return ;
            }
        }

        tasks.push(ApusData.Task(tasks.length + 1, 0, uniqID, address(0), input, _tp, ApusData.TaskStatus.Posted, new bytes(0), ri, expiry));
    }

    function dispatchTaskToClient(uint256 taskID) public {
        // address prover, uint256 cid, 

        for (uint256 i = 0; i < tasks.length; i++) {
            if (tasks[i].uniqID == taskID) {
                if (tasks[i]._stat == ApusData.TaskStatus.Posted) {
                    tasks[i]._stat = ApusData.TaskStatus.Assigned;
                    ApusData.ClientConfig memory cf;
                    (, cf) = market.getLowestN();

                    tasks[i].assigner = cf.owner;
                    tasks[i].clientId = cf.id;
                    market.dispatchTaskToClient(cf.owner, cf.id);
                }
            }
        }
    }

} 
