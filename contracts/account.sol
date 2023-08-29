// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;
import "openzeppelin-solidity/contracts/access/Ownable.sol";
contract AccountFactory is Ownable {

    struct accountInfo {
        address addr;
        uint balance;
        uint providerBlockedFunds;
        uint recipientBlockedFunds;
    }
    mapping (address => accountInfo) ownerToAccount;

    function register() public returns (accountInfo memory accountinfo) {
        accountInfo storage info = ownerToAccount[msg.sender];
        // 测试这里是否能判断key是否存在
        if (info.addr == address(0)) {
            info.addr = msg.sender;
            ownerToAccount[msg.sender] = info;
        }
        return info;
    }

    function withdraw() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    function cancellation() public  {
        delete(ownerToAccount[msg.sender]);
    }

    // 这里如何判断质押多少代币呢
    function stake() payable public {
        accountInfo storage info = ownerToAccount[msg.sender];
        if (info.addr == address(0)) {
            info.addr = msg.sender;
            info.balance = msg.value;
            ownerToAccount[msg.sender] = info;
            return ;
        }
        ownerToAccount[msg.sender].balance = ownerToAccount[msg.sender].balance + msg.value;
    }

    function unstake(uint amount) payable public {
        accountInfo memory info = ownerToAccount[msg.sender];
        require(info.balance >= amount, "amount not enough");
        ownerToAccount[msg.sender].balance = ownerToAccount[msg.sender].balance - amount;
        payable(msg.sender).transfer(amount);
    }

    // modifier _needAccountExist(address _user) {
    //     require(ownerToAccount[_user].addr == address(0), "need register first");
    //     _;
    // }
}

contract Provider is AccountFactory {
    // 上线机器后保证金
    function blockOnlineFund(uint _amout) internal {
    }

    // 下线机器后解冻保证金
    function unblockOfflineFund(uint _amout) internal {
    }
}

contract Recipient is AccountFactory {
    // 冻结支付产生的费用
    function blockRentFund(uint amount) internal {

    }

    // 冻结续租产生的费用    
    function blockRenewalFund(uint period) internal {

    }

    // 账单结算
    function settleFund(uint period) internal {
        
    }

}