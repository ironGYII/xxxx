// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;
import "./lease.sol";
import "./account.sol";
import "./device.sol";

contract Helper is Billing {

    AccountFactory public account_contract;

    constructor(address _accountFactoryAddress) {
        account_contract = AccountFactory(_accountFactoryAddress);
    }

    // function getAccountContract() private view returns(address)

    function rentServer(uint _deviceId, uint _endTime) public {
        // device rent
        uint _startTime = block.timestamp;
        deviceInfo memory dc = getDevice(_deviceId);
        rentDevice(_deviceId);
        uint _leaseId = createRentLease(_deviceId, _startTime, _endTime);
        uint _stakeAmount = recipientStakeCalcute(_startTime, _endTime, dc.price);
        createRentBilling(_leaseId, 10);
        account_contract.rentBlockedFund(msg.sender, 10);
    }

    // 续租
    function RenewalLeaseServer(uint _leaseId, uint _endTime) public {
        leaseInfo memory _lease  = renewalRentLease(_leaseId, _endTime);

        // device rent
        deviceInfo memory _dc = getDevice(_lease.deviceId);
        uint _stakeAmount = recipientStakeCalcute(_lease.startTime, _endTime, _dc.price);
        billingInfo memory _bi = getRecipientBillingByLeaseId(_leaseId);
        _stakeAmount = renewalRentBilling(_bi.id, _stakeAmount);
        account_contract.rentBlockedFund(msg.sender, _stakeAmount);
    }

    function terminateInstance(uint _leaseId) public {

        leaseInfo memory _lease  = terminateLease(_leaseId);

        terminateDevice(_lease.deviceId);
        // device rent
        deviceInfo memory _dc = getDevice(_lease.deviceId);

        uint _stakeAmount = recipientStakeCalcute(_lease.startTime, _lease.expireTime, _dc.price);

        billingInfo memory _bi = getRecipientBillingByLeaseId(_leaseId);

        uint _unBlockedAmount = terminateBilling(_bi.id, _stakeAmount);

        account_contract.rentUnBlockedFund(msg.sender, _dc.owner, _stakeAmount, _unBlockedAmount);
    }


    function onlineServer(string memory _machineId, string memory _serverInfo, Price memory _price, uint _startTime, uint _endTime) public {
        
        uint _stakeAmount = providerStakeCalcute(_startTime, _endTime, _price);
        account_contract.onlineBlockedFund(msg.sender, _stakeAmount);
        uint _deviceId = online(_machineId, _serverInfo, _price);
        uint _leaseId = onlineLease(msg.sender, _deviceId, _startTime, _endTime);
        providerOnlineBilling(_leaseId, _stakeAmount);
    }

    function offlineServer(uint _deviceId) public {
        offlineDevice(_deviceId);
        leaseInfo memory _pli = getLeaseByDeviceId(_deviceId);
        billingInfo memory _bi = getProviderBillingByLeaseId(_pli.leaseId);
        providerOfflineBilling(_bi.id);
        account_contract.offlineUnBlockedFund(msg.sender, _bi.providerBlockedFund);
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

    function listProviderLease(address _user, uint _limit, uint _offset) public view returns (leaseInfo [] memory, billingInfo[] memory) {
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

    function getOfflineLeaseAndBilling(uint _deviceId) public view returns(leaseInfo memory, billingInfo memory){
        leaseInfo memory _pli = getLeaseByDeviceId(_deviceId);
        billingInfo memory b = getProviderBillingByLeaseId(_pli.leaseId);
        return (_pli, b);
    }

    function getRecipientLease() public returns(billingInfo [] memory){
        return recipientBillings;
    }
}