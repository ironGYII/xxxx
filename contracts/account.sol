// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;

contract A {
    mapping (address => uint256) private _account;

    function Set(uint256 amount) public {
        _account[msg.sender] = _account[msg.sender] + amount;
    }
}

contract Account is A{

    function stake(uint256 amount) public {
        _account[msg.sender] = _account[msg.sender] + amount;
    }

    function get() public  {
        return _account[msg.sender];
    }
}