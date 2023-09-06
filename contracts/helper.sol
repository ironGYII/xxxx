// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;
import "./lease.sol";
import "./account.sol";
import "./device.sol";

// contract Helper is Lease, Device, Provider, Recipient {
contract Helper is Billing, AccountFactory {

    function onlineServer(string memory _machineId, string memory _serverInfo, Price memory _price, uint _startTime, uint _endTime) public {
        
        uint _stakeAmount = providerStakeCalcute(_startTime, _endTime, _price);
        onlineBlockedFund(_stakeAmount);
        uint _deviceId = online(_machineId, _serverInfo, _price);
        uint _leaseId = onlineLease(msg.sender, _deviceId, _startTime, _endTime);
        providerOnlineBilling(_leaseId, _stakeAmount);
    }

    function offlineServer(uint _deviceId) public {
        offlineDevice(_deviceId);
        providerLeaseInfo memory _pli = getLeaseByDeviceId(_deviceId);
        billingInfo memory _bi = getProviderBillingByLeaseId(_pli.leaseId);
        providerOfflineBilling(_bi.id);
        offlineUnBlockedFund(_bi.providerBlockedFund);
    }

    function listDevices(uint _limit, uint _offset) public view returns (deviceInfo [] memory _allDevices){
        deviceInfo [] memory ds = new deviceInfo[](_limit);
        uint counter = 0;
        for (uint i = _offset * _limit; i < devices.length; i++ ) {
            if (devices[i].status == DeviceStatus.Online || devices[i].status == DeviceStatus.Running ) {
                if (counter < _limit) {
                    ds[counter] = devices[i];
                    counter ++;
                }

                if  (counter >= _limit * (_offset + 1)) {
                    return ds;
                }
            }
        }
        return ds;
    }

    function listOwnDevices(address _provider, uint _limit, uint _offset) public view returns (deviceInfo [] memory _ownDevices){
        deviceInfo [] memory ds = new deviceInfo [](_limit);
        uint counter = 0;
        for (uint i = _offset * _limit; i < devices.length; i++ ) {
            if (devices[i].owner == _provider) {
                if (counter < _limit) {
                    ds[counter] = devices[i];
                    counter ++;
                }
                if  (counter >= _limit * (_offset + 1)) {
                    return ds;
                }
            }
        }
        return ds;
    }

    function listProviderLease(address _user, uint _limit, uint _offset) public view returns (providerLeaseInfo [] memory, billingInfo[] memory) {
        _limit = _limit + _offset;
        _user = _user;
        return (leaseProvider, providerBillings);
        // providerLeaseInfo [] memory _ls = new providerLeaseInfo[] (_limit);
        // uint counter = 0;
        // for (uint i = 0; i < leaseProvider.length; i++ ) {
        //     if (leaseProvider[i].owner== _user ) {
        //         if (counter > _limit * _offset) {
        //             _ls[counter] = leaseProvider[i];
        //             counter ++;
        //         }

        //         if  (counter >= _limit * _offset) {
        //             return _ls;
        //         }
        //     }
        // }
        // return _ls;
    }

    function getOfflineLeaseAndBilling(uint _deviceId) public view returns(providerLeaseInfo memory, billingInfo memory){
        providerLeaseInfo memory _pli = getLeaseByDeviceId(_deviceId);
        billingInfo memory b = getProviderBillingByLeaseId(_pli.leaseId);
        return (_pli, b);
    }

}