
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

    function submitTask(uint256 taskID, bytes calldata result) public {
        require(tasks[taskID - 1]._stat == ApusData.TaskStatus.Assigned);
        tasks[taskID - 1]._stat = ApusData.TaskStatus.Done;
        tasks[taskID - 1].result = result;
        market.releaseTaskToClient(tasks[taskID - 1].assigner, tasks[taskID - 1].clientId);

        token.reward(tasks[taskID - 1].assigner);
    }

    function postTask(ApusData.TaskType _tp, uint256 uniqID, bytes calldata input, uint64 expiry, ApusData.rewardInfo memory ri) public {
        for (uint256 i = 0; i < tasks.length; i++) {
            if (tasks[i]._tp ==  _tp && tasks[i].uniqID == uniqID) {
                return ;
            }
        }

        tasks.push(ApusData.Task(tasks.length + 1, 0, uniqID, address(0), input, _tp, ApusData.TaskStatus.Posted, new bytes(0), ri, expiry));
    }

    function dispatchTaskToClient(address prover, uint256 cid, uint256 taskID) public {
        require(tasks[taskID - 1]._stat == ApusData.TaskStatus.Posted);
        tasks[taskID - 1]._stat = ApusData.TaskStatus.Assigned;
        tasks[taskID - 1].assigner = prover;
        tasks[taskID - 1].clientId = cid;
        market.dispatchTaskToClient(prover, cid);
    }

} 
