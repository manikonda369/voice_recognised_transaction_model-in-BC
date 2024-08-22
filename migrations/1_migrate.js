const SimpleBank = artifacts.require("SimpleBank");

module.exports = function(deployer) {
  // Pass the constructor argument here
//   const ownerName = "Kumar"; // Set the owner name here

  deployer.deploy(SimpleBank);
};
