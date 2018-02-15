import requests as rq
import json
import time

class BlockChainData:

    def __init__(self, secret, address):
        self.secret = secret
        self.address = address


    def buildAsset(self, createTime, pickupTime, deliveryTime, price, quantity, maxTemperature, minTemperature, toleranceTime, measureInterval, penaltyMoneyUnit, penaltyTimeUnit, maxPenalty, bcSyncInterval, incoterm):
        data = {
            'content': {
                'secret': self.secret,
                'data': {
                    'name': incoterm,
                    'owner': self.address,
                    'creator': self.address,
                    'created_at': createTime,
                    'custom': {
                        'pickup_time': pickupTime,
                        'delivery_time': deliveryTime,
                        'price': price,
                        'quantity': quantity,
                        'max_temperature': maxTemperature,
                        'min_temperature': minTemperature,
                        'tolerance_time': toleranceTime,
                        'measure_interval': measureInterval,
                        'penalty_money_unit': penaltyMoneyUnit,
                        'penalty_time_unit': penaltyTimeUnit,
                        'max_penalty': maxPenalty,
                        'bcSyncInterval': bcSyncInterval
                    }
                },
                'identifiers': {
                    'isbn': '123'
                }
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        r = rq.post('https://network.ambrosus.com/assets', json=data, headers=headers)


    #def buildEvent():
    #    pass
#
#
    #def getEventsByAssetId():
    #    pass

if __name__ == '__main__':
    secret = '0x546de93a45c8df31e63b0bea9534a7ca03e9eb0e817f0d436d9b324b43d0a123'
    address = '0xdce2dd4bB3A9E29714dD317d05869fcD72F20Cbe'
    bcd = BlockChainData(secret, address)
    bcd.buildAsset(1518685688, 1518685688, 1518688000, 1000, 1, 50, 5, 100, 10, 10, 100, 500, 10, 'hah')
