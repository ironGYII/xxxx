// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

library ApusData {

    // prover zkEVM client 
    struct ClientConfig {
        string url;
        uint256 minFee;
        uint8 maxZkEvmInstance;
        uint8 curInstance;
    }


    struct ProverClient {
        address owner;
        // prover stake to apus
        mapping(address => uint256) stakeAmount;
        // apus lock amount when assigned prover proof task
        mapping(address => uint256) lockAmount;
        ClientConfig[] clients;
    }


    enum TaskType {TaikoZKEvm}
    enum TaskStatus {Assigned, Proving, Proved, Rewarded, Slashed}
    // proof task info
    struct ProofTask {
        TaskType _type;
        // todo(yuanming): 其他必须记录的消息, 目前还不确定
    }

    // 
    struct binding {
        address prover;
        TaskStatus status;
        ProofTask task;
        // mapping(user mapping(erc20 address, amount))
        mapping(address => mapping (address => uint)) lockAmount; 
    }
}

