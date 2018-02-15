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
        #print(r.text)
        return r.text
    #    pass
#
#
    def buildEvent(self, AssetId, createTime, TempSensor1, TempSensor2, TempSensor3, Humidity, UnitTemp, UnitHumidity):
        data = {
            'content': {
                'secret': self.secret,
                'data': {
                    'type': 'measurement.temperature',
                    'subject': "0x44EA4BAe7C8176690102cBf83d87FAD2bD6F1F27",
                    'creator': "0x44EA4BAe7C8176690102cBf83d87FAD2bD6F1F27",
                    'created_at': createTime,
                    'tempSensor1': TempSensor1,
                    'tempSensor2': TempSensor2,
                    'tempSensor3': TempSensor3,
                    'humidity': Humidity,
                    'unitTemp': 'Celcius'
                    'unitHum' : 'Percent'
                    }
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        r = rq.post('https://network.ambrosus.com/assets/{}/events'.format(AssetId), json=data, headers=headers)
        print(r.text)
    #def getEventsByAssetId():
    #    pass

if __name__ == '__main__':
    secret = '0x546de93a45c8df31e63b0bea9534a7ca03e9eb0e817f0d436d9b324b43d0a123'
    address = '0xdce2dd4bB3A9E29714dD317d05869fcD72F20Cbe'
    bcd = BlockChainData(secret, address)
    asset = bcd.buildAsset(1518685688, 1518685688, 1518688000, 1000, 1, 50, 5, 100, 10, 10, 100, 500, 10, 'hah')
    bcd.buildEvent(asset['id'], 1518685688, 8, 12, 10, 40, 'Celcius', 'Percent')
