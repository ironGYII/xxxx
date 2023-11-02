// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./console.sol";
// import "./LibMarket.sol";

contract IronGYI {
    // Search the n'st lowest price prover 
    uint256 n = 0;

    function get() public view returns(uint256){
        console.log('count: %d', n);
        console.log();
        return n;
    }

    function set(uint256 _n) public returns(uint256) {
        n = _n;
        console.log('count: %d', n);
        return n;
    }
}