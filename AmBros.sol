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
    address logistic;
    /*
    address ownerAMB;
    address creatorAMB;
    */
    status stat;
  }

  Order[] public orders;

  function confirm(uint256 orderId, uint256 finalPrice) public {
    Order storage order = orders[orderId];
    require(order.stat == status.Active);
    uint256 returnPrice = order.shippingPrice - finalPrice;
    require(this.balance >= returnPrice);
    order.customer.transfer(returnPrice);
    order.logistic.transfer(finalPrice);
    order.stat = status.Done;
  }

  function newOrder(address logistic, uint256 shippingPrice) public payable {
    require(msg.value == shippingPrice);
    uint256 orderId = orders.length++;
    Order storage order = orders[orderId];
    order.orderId = orderId;
    order.customer = msg.sender;
    order.logistic = logistic;
    order.shippingPrice = shippingPrice;
    order.stat = status.Active;
  }
}
