// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;

enum DeviceStatus {Created, Online, Running, Offline}

struct deviceInfo {
        address owner;
        uint id;
        // uint8 status;
        DeviceStatus status;
        uint price;
        string extraData;

}

contract DeviceFactory {
    uint id = 0;
    deviceInfo [] public devices;

    modifier _isOwner(address _owner) {
        _;
    }

    function createDevice(uint _price, string memory _extraData) internal {
        id += 1;
        devices.push(deviceInfo(msg.sender, id, DeviceStatus.Created, _price, _extraData));
    }

    function deleteDevices(uint _deviceId) internal {
        require(devices[_deviceId].status == DeviceStatus.Online || devices[_deviceId].status == DeviceStatus.Created, "need pre status online or created");
        devices[_deviceId - 1].status = DeviceStatus.Offline;
    }

}


contract Device is DeviceFactory {

    modifier canRent(string memory _deviceId) {
        _;
    }

    function onlineDevice(uint _deviceId) internal {
        require(devices[_deviceId].status == DeviceStatus.Created, "need pre status created");
        devices[_deviceId].status = DeviceStatus.Online;
    }

    function offlineDevice(uint _deviceId) internal {
        require(devices[_deviceId].status == DeviceStatus.Online || devices[_deviceId].status == DeviceStatus.Created, "need pre status online or created");
        devices[_deviceId].status = DeviceStatus.Offline;
        if (devices[_deviceId].status == DeviceStatus.Online) {
        }
    }

    function rentDevice(uint _deviceId) internal {
        require(devices[_deviceId].status == DeviceStatus.Online , "need pre status online");
        devices[_deviceId].status = DeviceStatus.Running;
    }

    function expireDevice(uint _deviceId) internal {
        require(devices[_deviceId].status == DeviceStatus.Running, "need pre status running");
        devices[_deviceId].status = DeviceStatus.Online;
    }

}