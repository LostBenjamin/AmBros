pragma solidity ^0.4.18;

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
    uint256 orderNumber;
    uint256 shippingPrice;
    address customer;
    address logistic;
    status stat;
  }

  mapping (uint256 => Order) public orders;

  function confirm(uint256 orderNumber, uint256 finalPrice) public {
    Order storage order = orders[orderNumber];
    require(order.stat == status.Active);
    uint256 returnPrice = order.shippingPrice - finalPrice;
    require(this.balance >= returnPrice);
    order.customer.transfer(returnPrice);
    order.logistic.transfer(finalPrice);
    order.stat = status.Done;
  }

  function newOrder(address logistic, uint256 orderNumber, uint256 shippingPrice) public payable {
    require(msg.value == shippingPrice);
    orders[orderNumber] = Order(orderNumber, shippingPrice, msg.sender, logistic, status.Active);
  }
}
