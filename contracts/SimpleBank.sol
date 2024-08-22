// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract SimpleBank {
    uint8 private clientCount;
    mapping(address => UserInfo) private users;
    mapping(address => bool) private enrolled;
    mapping(string => address) private addressByName; // Reverse mapping of names to addresses
    address public owner;

    event LogDepositMade(string indexed userName, uint amount);
    event LogWithdrawalMade(string indexed userName, uint amount);
    event LogTransfer(string indexed from, string indexed to, uint amount);
    event LogEnrolled(address indexed accountAddress, string name);
    event LogUnenrolled(string indexed userName);
    event LogTransaction(string indexed from, string indexed to, uint amount, uint timestamp);

    struct UserInfo {
        string name;
        uint balance;
    }

    struct Transaction {
        string from;
        string to;
        uint amount;
        uint timestamp;
    }

    Transaction[] private transactionHistory;

    modifier onlyOwner() {
        require(msg.sender == owner, "Only contract owner can call this function");
        _;
    }

    constructor() {
        owner = msg.sender;
        clientCount = 0;
    }

    function addToTransactionHistory(string memory from, string memory to, uint amount) private {
        uint timestamp = block.timestamp;
        Transaction memory transaction = Transaction(from, to, amount, timestamp);
        transactionHistory.push(transaction);
        emit LogTransaction(from, to, amount, timestamp);
    }

    function enroll(address accountAddress, string memory name) public onlyOwner {
        require(clientCount < 3, "Maximum client limit reached");
        require(!enrolled[accountAddress], "Account is already enrolled");
        require(addressByName[name] == address(0), "Name is already registered");

        enrolled[accountAddress] = true;
        clientCount++;
        users[accountAddress] = UserInfo(name, 0);
        addressByName[name] = accountAddress;
        emit LogEnrolled(accountAddress, name);
    }

    function unenroll(string memory name) public onlyOwner {
        require(addressByName[name] != address(0), "No account is enrolled with this name");

        address accountAddress = addressByName[name];
        delete enrolled[accountAddress];
        delete users[accountAddress];
        delete addressByName[name];
        clientCount--;

        emit LogUnenrolled(name);
    }

    function deposit(uint amount) public {
    string memory userName = users[msg.sender].name;
    address accountAddress = addressByName[userName];
    require(enrolled[accountAddress], "Account is not enrolled");
    require(amount > 0, "Deposit amount must be greater than zero");

    users[accountAddress].balance += amount;
    emit LogDepositMade(userName, amount);
    addToTransactionHistory(userName, userName, amount);
}


    function withdraw(uint withdrawAmount) public onlyOwner {
        string memory userName = users[msg.sender].name;
        address accountAddress = addressByName[userName];
        require(enrolled[accountAddress], "Account is not enrolled");
        require(withdrawAmount <= users[accountAddress].balance, "Insufficient balance");

        users[accountAddress].balance -= withdrawAmount;
        payable(msg.sender).transfer(withdrawAmount);

        emit LogWithdrawalMade(userName, withdrawAmount);
        addToTransactionHistory(userName, userName, withdrawAmount);
    }

    function transfer(string memory to, uint amount) public onlyOwner {
        string memory from = users[msg.sender].name;
        address fromAddress = msg.sender;
        require(addressByName[to] != address(0), "Recipient is not enrolled");
        require(amount <= users[fromAddress].balance, "Insufficient balance");

        address toAddress = addressByName[to];

        users[fromAddress].balance -= amount;
        users[toAddress].balance += amount;

        emit LogTransfer(from, to, amount);
        addToTransactionHistory(from, to, amount);
    }

    function balanceOf() public view returns (uint) {
        address accountAddress = addressByName[users[msg.sender].name];
        return users[accountAddress].balance;
    }

    function totalBalance() public view returns (uint) {
        return address(this).balance;
    }

    function getOwner() public view returns (address) {
        return owner;
    }

    function isEnrolled(string memory userName) public view returns (bool) {
        address accountAddress = addressByName[userName];
        return enrolled[accountAddress];
    }

    function getAddressByName(string memory userName) public view returns (address) {
        return addressByName[userName];
    }

    function getTransactionHistory() public view returns (Transaction[] memory) {
        return transactionHistory;
    }
}