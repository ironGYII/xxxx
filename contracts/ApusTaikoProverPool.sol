// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {TaikoData} from "./TaikoData.sol";
import {ApusData} from "./ApusData.sol";
import {IReward, IProver, IProofTask} from "./ApusInterface.sol";

// 创建一个接口来表示 ERC20 代币合约
interface IERC20Mintable {
    function mint(address to, uint256 amount) external;
}

contract ApusTaikoProverPool is IProver, IReward {
    address private owner;

    constructor() {
        owner = msg.sender;
    }

    // 定义一个修饰符，用于检查调用者是否是合约的拥有者
    modifier onlyOwner {
        require(msg.sender == owner, "Caller is not owner");
        _;
    }

    // IProofTask合约地址
    address public proofTaskContract;
    // Apus ERC20合约地址
    address public apusTokenContract;

    // 设置IProofTask合约地址
    function setProofTaskContract(address _proofTaskContract) external {
        proofTaskContract = _proofTaskContract;
    }

    // 获取IProofTask合约地址
    function getProofTaskContract() external view returns (address) {
        return proofTaskContract;
    }

    struct Reward {
        address prover;
        uint64 expiry;
        uint256 amount;
    }
    
    event RewardTransfered(
        uint64 blockId,
        address prover,
        uint256 amount
    );

    // blockID对应的奖励
    mapping(uint64 => Reward) public rewards;

    function convert(string memory source) public pure returns (bytes32 result) {
        bytes memory tempEmptyStringTest = bytes(source);
        if (tempEmptyStringTest.length == 0) {
            return 0x0;
        }

        assembly {
            result := mload(add(source, 32))
        }
    }

    function onBlockAssigned(
        uint64 blockId,
        TaikoData.BlockMetadataInput calldata input,
        TaikoData.ProverAssignment calldata assignment
    ) external payable {
        // 解析assignment.data -> ProofAssignment
        ApusData.ProofAssignment memory apusAssignment = abi.decode(assignment.data, (ApusData.ProofAssignment));
        // 调用IProofTask的bindTask方法
        IProofTask(proofTaskContract).bindTask(
            ApusData.TaskType.TaikoZKEvm,
            blockId,
            abi.encode(input),
            apusAssignment
        );
        // 记录奖励
        rewards[blockId] = Reward({
            prover: apusAssignment.prover,
            expiry: assignment.expiry,
            amount: msg.value
        });
    }

    function reward(uint64 blockId) external payable onlyOwner {
        // 查询奖励
        Reward memory rewardList = rewards[blockId];
        // 发送奖励
        payable(rewardList.prover).transfer(rewardList.amount);
        // 触发事件
        emit RewardTransfered(blockId, rewardList.prover, rewardList.amount);
    }

    function rewardApusToken(uint256 amount) external onlyOwner {
        // ERC20合约 mint token
        IERC20Mintable(apusTokenContract).mint(address(this), amount);
        // 分配token，待定
    }
}
