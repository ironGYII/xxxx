// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;
import "openzeppelin-solidity/contracts/access/Ownable.sol";
import {ApusToken} from "./token.sol";
import {Lease} from "./lease.sol";

contract Account {

    ApusToken private _apusToken;
    Lease private _leaseManager;

    mapping (address => uint256) private  _stakeAmount;
    mapping (address => uint256) private _depositAmount;

    function stake(uint256 amount) uint256 {
        
    }
}