var MyContract = artifacts.require("helper.sol");

module.exports = function(deployer) {
    // 部署步骤
    deployer.deploy(MyContract);
  };