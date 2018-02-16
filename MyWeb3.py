from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract

class MyWeb3():

    def __init__(self, logisticAddress, consumerAddress, deployerAddress, solPath):
        self.logisticAddress = logisticAddress
        self.consumerAddress = consumerAddress
        self.deployerAddress = deployerAddress
        #self.web3 = Web3(HTTPProvider('https://ropsten.infura.io/ESsNRSGHG447qbNzmJBW'))
        self.web3 = Web3(HTTPProvider('http://localhost:8545'))

        compiledSol = compile_source(open(solPath).read())
        contractInterface = compiledSol['<stdin>:DeliveryCondition']
        contract = self.web3.eth.contract(abi=contractInterface['abi'], bytecode=contractInterface['bin'])
        txHash = contract.deploy(transaction={'from': self.deployerAddress})
        txReceipt = self.web3.eth.getTransactionReceipt(txHash)
        self.contractAddress = txReceipt['contractAddress']
        self.contractInstance = self.web3.eth.contract(contractInterface['abi'], self.contractAddress, ContractFactoryClass = ConciseContract)


    def getLogisticBalance(self):
        return self.web3.eth.getBalance(self.logisticAddress)


    def getConsumerBalance(self):
        return self.web3.eth.getBalance(self.consumerAddress)


    def getContractBalance(self):
        return self.web3.eth.getBalance(self.contractAddress)


    def createOrder(self, orderNumber, shippingPrice):
        self.contractInstance.newOrder(self.logisticAddress, orderNumber, shippingPrice, transact={'from': self.consumerAddress, 'value': shippingPrice})


    def confirm(self, orderNumber, finalPrice):
        self.contractInstance.confirm(orderNumber, finalPrice, transact={'from': self.consumerAddress})


if __name__ == '__main__':
    #ropsten
    logisticAddress = '0x98b0ac8BEc2ea87d38BA2325D296822B71949689'
    consumerAddress = '0xaA8c5571befc412288254468AAcbdD033dA21Bf5'
    deployerAddress = '0x79c6dcE7863D7fa5F8B6784D532681173627b4f4'

    #testrpc
    logisticAddress = '0x5ccffcac6912d273aa5cbd27dad717e00de96c0e'
    consumerAddress = '0xaae032eb0e649a7fa7b8e249a6efc9f5b4c7a9cd'
    deployerAddress = '0xda7ef6552c72db698ae194bb842c57867a8e9a19'

    myweb3 = MyWeb3(logisticAddress, consumerAddress, deployerAddress, 'AmBros.sol')
    print(myweb3.getLogisticBalance())
    print(myweb3.getConsumerBalance())
    myweb3.createOrder(1, 1000)
    print(str(myweb3.contractInstance.orders(1)))
    myweb3.confirm(1, 500)
    print(str(myweb3.contractInstance.orders(1)))
    print(myweb3.getLogisticBalance())
    print(myweb3.getConsumerBalance())
    #myweb3.contractInstance.confirm(0, 500, transact={'from': myweb3.consumerAddress, 'gas': 400000})

    #myweb3.contractInstance.haha(myweb3.logisticAddress, transact={'from': myweb3.consumerAddress, 'gas': 40000, 'value':1000})
    #myweb3.contractInstance.transact({'from': myweb3.consumerAddress, 'gas': 500000}).newOrder(myweb3.logisticAddress, 0, 1000)
    #myweb3.contractInstance.functions.newOrder(myweb3.logisticAddress, 0, 1000).transact()
