// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

library ApusData {



    // prover zkEVM client 
    struct ClientConfig {
        address owner;
        uint256 id;
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

    struct rewardInfo {
        address token; // token address, eth if 0
        uint256 amount;
    }

    struct Task {
        uint256 id;
        uint256 clientId;
        uint256 uniqID;
        address assigner;
        bytes input;
        TaskType _tp;
        TaskStatus _stat;
        bytes result;
        rewardInfo reward;
        uint64 expiry;
    }


    enum TaskType {TaikoZKEvm}
    enum TaskStatus {Posted, Assigned, Done, Slashed}
    
}
