const fs = require('fs');
const path = require('path');
var BindingContract = artifacts.require("Binding");

module.exports = function (deployer) {
 
deployer.deploy(BindingContract).then(() => {
      if (BindingContract.networks[deployer.network_id]) {
        const contractAddress = BindingContract.networks[deployer.network_id].address;
        const contractData = {
          address: contractAddress
        };
        const directoryPath = path.join(__dirname, '../', 'build', 'contract_address');
        const filePath = path.join(directoryPath, 'Binding.json');

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