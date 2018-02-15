import requests as rq
import json
import time

class BlockChainAsset:

    def __init__(self, secret, address):
        self.secret = secret
        self.address = address
        self.assetId = None


    def buildAsset(self, orderNumber, createTime, pickupTime, deliveryTime, shippingPrice, quantity, maxTemperature, minTemperature, toleranceTime, measureInterval, penaltyPerday, maxPenalty, bcSyncInterval, incoterm):
        data = {
            'content': {
                'secret': self.secret,
                'data': {
                    'name': incoterm,
                    'owner': self.address,
                    'creator': self.address,
                    'created_at': createTime,
                    'custom': {
                        'order_number': orderNumber,
                        'pickup_time': pickupTime,
                        'delivery_time': deliveryTime,
                        'shipping_price': shippingPrice,
                        'quantity': quantity,
                        'max_temperature': maxTemperature,
                        'min_temperature': minTemperature,
                        'tolerance_time': toleranceTime,
                        'measure_interval': measureInterval,
                        'penalty_per_day': penaltyPerday,
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
        j = json.loads(r.text)
        self.assetId = j['id']


    def buildEvent(self, tempSensor1, tempSensor2, tempSensor3, createTime):
        data = {
            'content': {
                'secret': self.secret,
                'data': {
                    'type': 'measurement.temperature',
                    'subject': self.assetId,
                    'creator': self.address,
                    'created_at': createTime,
                    'custom': {
                        'tempSensor1': tempSensor1,
                        'tempSensor2': tempSensor2,
                        'tempSensor3': tempSensor3,
                        'unit': 'Celcius'
                        }
                    }
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        r = rq.post('https://network.ambrosus.com/assets/{}/events'.format(self.assetId), json=data, headers=headers)


    def getEvents(self):
        headers = {
            'Content-Type': 'application/json'
        }
        r = rq.get('https://network.ambrosus.com/assets/{}/events'.format(self.assetId), headers=headers)
        #print(json.dumps(json.loads(r.text), indent = 4, sort_keys = True))
        return json.loads(r.text)


if __name__ == '__main__':
    secret = '0x546de93a45c8df31e63b0bea9534a7ca03e9eb0e817f0d436d9b324b43d0a123'
    address = '0xdce2dd4bB3A9E29714dD317d05869fcD72F20Cbe'
    bca = BlockChainAsset(secret, address)
    asset = bca.buildAsset(0, 1518685688, 1518685688, 1518688000, 1000, 1, 50, 5, 100, 10, 100, 500, 10, 'hah')
    bca.buildEvent(8, 12, 10, 1518685688)
    bca.buildEvent(9, 13, 11, 1518685800)
    bca.getEvents()
