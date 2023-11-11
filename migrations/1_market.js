const fs = require('fs');
const path = require('path');
var MarketContract = artifacts.require("Market");
var TaskContract = artifacts.require("ApusProofTask");
var TokenContract = artifacts.require("ERC20");

module.exports = function(deployer) {
  let marketInstance;
  let proofTaskInstance;
  let tokenInstance;

  deployer.deploy(MarketContract)
    .then(instance => {
      marketInstance = instance;
    // constructor( uint256 _initialAmount, string memory _tokenName, uint8 _decimalUnits, string memory _tokenSymbol) {
      return deployer.deploy(TokenContract, 10000000000, "apus token", 18, "at");
    })
    .then(instance => {
      tokenInstance = instance;
      return deployer.deploy(TaskContract, marketInstance.address, tokenInstance.address);
    })
    .then(instance => {
      proofTaskInstance = instance;
      return marketInstance.setTask(proofTaskInstance.address);
    })
    .then(() => {
      // 在这里可以执行其他与部署顺序无关的操作
        const directoryPath = path.join(__dirname, '../', 'build', 'contract_address');
        const marketPath = path.join(directoryPath, 'Market.json');
        const taskPath = path.join(directoryPath, 'ApusProofTask.json');
        // 创建目录
        if (!fs.existsSync(directoryPath)) {
            fs.mkdirSync(directoryPath, { recursive: true });
         }

        fs.writeFileSync(marketPath, JSON.stringify({address: MarketContract.networks[deployer.network_id].address}, null, 2));
        fs.writeFileSync(taskPath, JSON.stringify({address: TaskContract.networks[deployer.network_id].address}, null, 2));
        // console.log(`Contract address saved to ${filePath}`);
    });
};