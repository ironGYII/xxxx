// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;

import "./device.sol";

enum leaseType {Machine, Developer}
enum billingStatus {UnPayed, Payed, UnValid}
enum billingType {ProviderStake, DeveloperRent, TreasureBilling}

struct billingInfo {
    address user;
    // 质押的token, 后续需要返还账户
    uint id;
    uint leaseId;
    uint providerBlockedFund;
    uint recipientBlockedFunds;
    // 涉及的金额
    uint amount;  // 结算时候, 才会出现, 跟lease有关
    billingStatus status;
    billingType billType;
}

struct providerLeaseInfo {
    address owner;
    uint leaseId;
    uint startTime;
    uint expireTime;
    uint deviceId;
}

contract Lease is Device {
    uint private leaseId = 0;
    uint8 public platformSharingRatio = 0;


    providerLeaseInfo [] public leaseProvider;
    // leaseInfo [] public leaseDeveloper;

    function onlineLease(address _owner, uint _devcieId, uint _startTime, uint _endTime) internal returns(uint){
        leaseId = leaseId + 1;
        // deviceInfo memory device = devices[_devcieId];
        leaseProvider.push(providerLeaseInfo(_owner, leaseId, _startTime, _endTime, _devcieId));
        return leaseId;
    }

    function providerStakeCalcute(uint _startTime, uint _endTime, Price memory _price) pure public returns(uint) {
        return _price.serverPrice * (_endTime - _startTime);
    }

    function getLeaseByDeviceId(uint _deviceId) view public returns(providerLeaseInfo memory) {
        for (uint i = 0; i < leaseProvider.length; i++) {
            if (leaseProvider[i].deviceId == _deviceId) {
                return leaseProvider[i];
            }
        }

        revert("can't find lease!");
    }


    // function renewalLease(uint _leaseId, uint _period) internal {

    //     uint _index = 0;
    //     (, _index) = getLeaseInfo(_leaseId);
    //     require(leases[_index].recipient == msg.sender, "only recipient can renewal lease");
    //     require(leases[_index].expireTime > block.timestamp, "lease always expire");

    //     leases[_index].expireTime = leases[_index].expireTime + _period;
    //     leases[_index].billing.fee = leases[_index].billing.fee + _period * (leases[_index].expireTime- leases[_index].startTime);
    // }

    // function expireLease(uint _leaseId) internal returns (uint index, billingInfo memory bInfo){
    //     uint _index;
    //     // leaseInfo memory _lInfo;
    //     (, _index) = getLeaseInfo(_leaseId);
        
    //     leases[_index].billing.status = billingStatus.payed;
    //     return (_index, leases[_index].billing);
    // }

    // function getLeaseInfo(uint _leaseId) private view returns (leaseInfo memory info, uint index){
    //     for (uint i = 0; i < leases.length; i++) {
    //         if (leases[i].leaseId == _leaseId) {
    //             return (leases[i], i);
    //         }
    //     }
    //     revert(concatenateStrings("unknown lease_id: ", uintToString(_leaseId)));
    // }

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
        uint256 _index = digits - 1;
        
        while (number != 0) {
            buffer[_index--] = bytes1(uint8(48 + number % 10));
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

contract Billing is Lease {
    uint private providerBillingCounter = 0;
    billingInfo [] public providerBillings;

    function getProviderBillingByLeaseId(uint _leaseId) view public returns(billingInfo memory) {
        for (uint i = 0; i < providerBillings.length; i++) {
            if (providerBillings[i].leaseId == _leaseId) {
                return providerBillings[i];
            }
        }
        revert("can't find billing!");
    }

    function providerOfflineBilling(uint _billId) internal {
        if (providerBillings[_billId - 1].status == billingStatus.Payed) {
            revert("stake amount has already unblocked");
        }
        providerBillings[_billId - 1].status = billingStatus.Payed;
    }

    function providerOnlineBilling(uint _leaseId, uint _stakeAmount) internal {
        // 生成一个账单, 
        providerBillingCounter = providerBillingCounter + 1;
        providerBillings.push(billingInfo(msg.sender, providerBillingCounter, _leaseId, _stakeAmount, 0, 0, billingStatus.UnPayed, billingType.ProviderStake));
    }
}


// struct billingInfo {
//     address user;
//     // 质押的token, 后续需要返还账户
//     uint providerBlockedFund;
//     uint recipientBlockedFunds;
//     // 涉及的金额
//     uint amount;  // 结算时候, 才会出现, 跟lease有关
//     billingStatus status;
//     billingType billType;
// }