const fs = require('fs');
const path = require('path');
var ApusIProverContract = artifacts.require("ApusTaikoProverPool");

module.exports = function (deployer) {
 
deployer.deploy(ApusIProverContract, "0xC2600C80Beb521CC4E2f1b40B9D169c46E391390").then(() => {
      if (ApusIProverContract.networks[deployer.network_id]) {
        const contractAddress = ApusIProverContract.networks[deployer.network_id].address;
        const contractData = {
          address: contractAddress
        };
        const directoryPath = path.join(__dirname, '../', 'build', 'contract_address');
        const filePath = path.join(directoryPath, 'ApusTaikoProverPool.json');

        // 创建目录
        if (!fs.existsSync(directoryPath)) {
            fs.mkdirSync(directoryPath, { recursive: true });
         }

        fs.writeFileSync(filePath, JSON.stringify(contractData, null, 2));
        console.log(`Contract address saved to ${filePath}`);
      } else {
        console.error('Contract deployment failed');
      }
    });
};