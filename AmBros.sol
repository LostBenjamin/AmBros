pragma solidity "0.4.18";

contract Owned {
  address public owner;

  function Owned() public {
    owner = msg.sender;
  }

  modifier onlyOwner() {
    require(owner == msg.sender);
    _;
  }
}

contract DeliveryCondition is Owned {
  address public oracleAddress;

  enum status {Active, Done}

  struct Order {
    uint256 orderId;
    uint256 shippingPrice;

    /*
    uint256 createTime;
    uint256 pickupTime;
    uint256 deliveryTime;
    uint256 price;
    uint256 quantity;
    int256 maxTemperature;
    int256 minTemperature;
    uint256 toleranceTime;
    uint256 measureInterval;
    uint256 penaltyMoneyUnit;
    uint256 penaltyTimeUnit;
    uint256 maxPenaly;
    uint256 bcSyncInterval;
    string incoterm;
    */

    address customer;
    /*
    address ownerAMB;
    address creatorAMB;
    */
    status stat;
  }

  Order[] public orders;
  mapping (uint256 => uint256) queries;

  modifier onlyOracle() {
    require (msg.sender == oracleAddress);
    _;
  }

  function setOracle(address _oracleAddress) public onlyOwner {
    oracleAddress = _oracleAddress;
  }

  function __callback(uint256 queryId, uint256 finalPrice) public onlyOracle {
    uint256 orderId = queries[queryId];
    Order storage order = orders[orderId];
    require(order.stat == status.Active);
    uint256 returnPrice = order.shippingPrice - finalPrice;
    require(this.balance >= returnPrice);
    order.customer.transfer(returnPrice);
    order.stat = status.Done;
  }

  function newOrder(uint256 shippingPrice) public payable {
    require(msg.value == shippingPrice);
    uint256 orderId = orders.length++;
    uint256 queryId = DeliveryOracle(oracleAddress).query();
    Order storage order = orders[orderId];
    order.orderId = queryId;
    order.shippingPrice = shippingPrice;
    order.customer = msg.sender;
    order.stat = status.Active;
    queries[queryId] = orderId;
  }
}

contract Caller {
  function __callback(uint256 queryId, uint256 finalPrice) public;
}

contract DeliveryOracle is Owned {
  address[] public oracleCaller;

  function query() public returns (uint256 queryId) {
    queryId = oracleCaller.length++;
    oracleCaller[queryId] = msg.sender;
    return queryId;
  }

  function sendOracleData(uint256 queryId, uint256 finalPrice) public onlyOwner {
    require(oracleCaller[queryId] != 0x0);
    address callingContract = oracleCaller[queryId];
    oracleCaller[queryId] = 0x0;
    Caller(callingContract).__callback(queryId, finalPrice);
  }
}
