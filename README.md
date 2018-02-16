# AmBros
This is a Dapp for BIOTS 2018 hackathon in ETH Zurich. We aim to provide a better solution for the transportation of sensitive goods, especially chemical products, which should be preserved under certain condition like temperature. The transportation is between a consumer, who wants to send some goods, and a logistic company, who takes the responsibility for the transportation. The consumer first pays a certain shipping fee to the smart contract and the logistic company starts transportation. During transportation, multivariate data is collected through sensors and sent to block chain. After the transportation finishes, the money is paid from the smart contract to the logistic company. Part of the money may be paid back to the consumer if some conditions are not met.


# Framework
![Alt text](https://github.com/ETHBiots2018/AmBros/blob/master/software.png)

Balance: for querying the balance of logistic company, consumer and smart contract

Order: for consumer to place a order to logistic company.

Sensor: sensor data collected and uploaded to blockchain during transportation

Receive: check the package and pay.


# Files
AmBros.sol: the smart contract.

BlockChainAsset.py: interface for sending and receiving data from block chain.

MyWeb3.py: interface for using the smart contract through web3.py.

UI.py: the UI and how the whole thing works together.
