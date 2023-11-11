// SPDX-License-Identifier: MIT
// Abstract contract for the full ERC 20 Token standard
// https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md
pragma solidity ^0.8.20;


contract ERC20 {

    uint256 constant private MAX_UINT256 = 2**256 - 1;
    mapping (address => uint256) public balances;
    mapping (address => mapping (address => uint256)) public allowed;
    /*
    NOTE:
    The following variables are OPTIONAL vanities. One does not have to include them.
    They allow one to customise the token contract & in no way influences the core functionality.
    Some wallets/interfaces might not even bother to look at this information.
    */
    string public name;                   //fancy name: eg Simon Bucks
    uint8 public decimals;                //How many decimals to show.
    string public symbol;                 //An identifier: eg SBX
    address private owner;
    uint256 public mintPerYear;
    uint256 public totalSupply;

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);

    constructor( uint256 _initialAmount, string memory _tokenName, uint8 _decimalUnits, string memory _tokenSymbol) {
        owner = msg.sender;
        balances[msg.sender] = _initialAmount;               // Give the creator all initial tokens
        totalSupply = _initialAmount;                        // Update total supply
        name = _tokenName;                                   // Set the name for display purposes
        decimals = _decimalUnits;                            // Amount of decimals for display purposes
        symbol = _tokenSymbol;                               // Set the symbol for display purposes
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balances[msg.sender] >= _value);
        balances[msg.sender] -= _value;
        balances[_to] += _value;
        emit Transfer(msg.sender, _to, _value); //solhint-disable-line indent, no-unused-vars
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        uint256 _allowance = allowed[_from][msg.sender];
        require(balances[_from] >= _value && _allowance >= _value);
        balances[_to] += _value;
        balances[_from] -= _value;
        if (_allowance < MAX_UINT256) {
            allowed[_from][msg.sender] -= _value;
        }
        emit Transfer(_from, _to, _value); //solhint-disable-line indent, no-unused-vars
        return true;
    }

    function balanceOf(address _owner) public view returns (uint256 balance) {
        return balances[_owner];
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value); //solhint-disable-line indent, no-unused-vars
        return true;
    }

    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }

    uint256 rewardEpoch;
    uint256 rewardPerTask = 1000;
    mapping (uint256 => address[]) rewardCache;
    // todo: add auth verify
    function reward(address _prover) public {
        // rewardCache[block.number].push(_prover);
        // for (; rewardEpoch < block.number; rewardEpoch ++) {
        //     _mint(rewardEpoch);
        // }
        // _mint(block.number);
        totalSupply += rewardPerTask;
        balances[_prover] += rewardPerTask;

    }
    function setRewardPerTask(uint256 _reward)  public {
        rewardPerTask = _reward;
    }

    function mint(uint256 epoch) public {
        return _mint(epoch);
    }

    function getRewardEpoch() public view returns (uint256) {
        return rewardEpoch;
    }

    function _mintTokenAmount() private view returns (uint256) {
        // 以太坊的出块速度大概是30秒, 
        // need strategy, cur Empty, fixed amount 
        // 
        uint256 epochPerYear = 365 * 2 * 60 * 24;
        return mintPerYear / epochPerYear;
    }

    // function setMintPerYear(uint256 amount)

    function _mint(uint256 epoch) private {
        if (rewardCache[epoch].length <= 0 ) {
            return ;
        } 
        
        totalSupply += _mintTokenAmount();
        uint256 totalProverReward = _mintTokenAmount() * 60 / 100;
        uint256 _rewardPerTask = calcReward(totalProverReward, rewardCache[epoch].length);
        balances[owner] +=  _mintTokenAmount() - _rewardPerTask * rewardCache[epoch].length;
    
        for (uint256 i = 0; i < rewardCache[epoch].length; i ++ ) {
            balances[rewardCache[epoch][i]] += _rewardPerTask;
        }

    }

    function calcReward(uint256 a, uint256 b) private pure returns(uint256){
        if (a % b == 0) {
            return a / b;
        } else {
            return a / b + 1;
        }
    }
} 