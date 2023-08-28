// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;

import "./device.sol";

enum billingStatus {unPayed, payed, unValid}

struct billingInfo {
    address provider;
    address recipient;
    billingStatus status;
    uint fee;
}

struct leaseInfo {
    uint leaseId;
    uint startTime;
    uint expireTime;
    uint price;
    uint deviceId;
    uint8 platformSharingRatio;
    address provider;
    address recipient;
    billingInfo billing;
}

contract Lease is Device{
    uint private leaseId = 0;
    uint8 public platformSharingRatio = 0;


    leaseInfo [] public leases;

    function signLease(uint _startTime, uint _endTime, uint _devcieId, uint _price) internal {
        deviceInfo storage device = devices[_devcieId];
        leaseId = leaseId + 1;
        leases.push(leaseInfo(leaseId, _startTime, _endTime, _price, _devcieId, platformSharingRatio, device.owner, msg.sender, billingInfo(device.owner, msg.sender, billingStatus.unPayed, _price * (_endTime - _startTime))));
    }

    function renewalLease(uint _leaseId, uint _period) internal {

        uint index = 0;
        (, index) = getLeaseInfo(_leaseId);
        require(leases[index].recipient == msg.sender, "only recipient can renewal lease");
        require(leases[index].expireTime > now() , "lease always expire");

        leases[index].expireTime = leases[index].expireTime + _period;
        leases[index].billing.fee = leases[index].billing.fee + _period * (_endTime - _startTime);
    }

    function expireLease(uint _leaseId) internal returns (uint index, billingInfo memory bInfo){
        uint index = 0;
        leaseInfo memory lInfo;
        (, index) = getLeaseInfo(_leaseId);
        
        leases[index].billing.status = billingStatus.payed;
        return (index, leases[index].billing);
    }

    function getLeaseInfo(uint leaseId) private returns (leaseInfo memory info, uint index){
        for (uint i = 0; i < leases.length; i++) {
            if (leases[i].leaseId == leaseId) {
                return (leases[i], i);
            }
            revert(concatenateStrings("unknown lease_id: ", uintToString(leaseId)));
        }
    }

    function concatenateStrings(string memory a, string memory b) public pure returns (string memory) {
        bytes memory strA = bytes(a);
        bytes memory strB = bytes(b);

        bytes memory result = new bytes(strA.length + strB.length);
        
        uint256 k = 0;
        for (uint256 i = 0; i < strA.length; i++) {
            result[k++] = strA[i];
        }
        
        for (uint256 i = 0; i < strB.length; i++) {
            result[k++] = strB[i];
        }
        
        return string(result);
    }

    function uintToString(uint256 number) public pure returns (string memory) {
        if (number == 0) {
            return "0";
        }
        
        uint256 temp = number;
        uint256 digits;
        
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        
        bytes memory buffer = new bytes(digits);
        uint256 index = digits - 1;
        
        while (number != 0) {
            buffer[index--] = bytes1(uint8(48 + number % 10));
            number /= 10;
        }
        
        return string(buffer);
    }
}

// contract Billing is Lease{

//     function settle(billingInfo memory _billingInfo) internal {

//     }

//     function invalid(billingInfo memory _billInfo) internal{

//     }
// }