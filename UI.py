from math import ceil
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from functools import partial
from BlockChainAsset import BlockChainAsset
from MyWeb3 import MyWeb3

secret = '0x546de93a45c8df31e63b0bea9534a7ca03e9eb0e817f0d436d9b324b43d0a123'
address = '0xdce2dd4bB3A9E29714dD317d05869fcD72F20Cbe'

logisticAddress = '0xc69a2c3e8eaa8e901292d69eb5a7b683b81e7c4a'
consumerAddress = '0x30360b46c86bce97d67bc59ab2a874513860d258'
deployerAddress = '0x3f5a37d0189b233d2a70a83d1cfa581a25e7e34b'
myweb3 = MyWeb3(logisticAddress, consumerAddress, deployerAddress, 'AmBros.sol')

BALANCE = 'Balance'
ORDER = 'Order'
SENSOR = 'Sensor'
RECEIVE = 'Receive'
screenTexts = [BALANCE, ORDER, SENSOR, RECEIVE]

ORDER_NUMBER = 'Order Number'
CREATE_TIME = 'Creation Time'
PICKUP_TIME = 'Pickup Time'
DELIVERY_TIME = 'Delivery Time'
SHIPPING_PRICE = 'Shipping Price'
QUANTITY = 'Quantity'
MAX_TEMPERATURE = 'Max Temperature'
MIN_TEMPERATURE = 'Min Temperature'
TOLERANCE_TIME = 'Tolerance Time'
MEASURE_INTERVAL = 'Measure Interval'
PENALTY_PERDAY = 'Penalty Per Day'
MAX_PENALTY = 'Max Penalty'
BC_SYNC_INTERVAL = 'Block Chain Sync Interval'
INCOTERM = 'Incoterm'
assetTexts = [ORDER_NUMBER, CREATE_TIME, PICKUP_TIME, DELIVERY_TIME, SHIPPING_PRICE, QUANTITY, MAX_TEMPERATURE, MIN_TEMPERATURE, TOLERANCE_TIME, MEASURE_INTERVAL, PENALTY_PERDAY, MAX_PENALTY, BC_SYNC_INTERVAL, INCOTERM]

bcAsset = BlockChainAsset(secret, address)
orderData = dict()

payBack = 0
payToDelivery = 0

def submit(btn):
    global orderData
    data = dict(map(lambda t: (t, btn.father.entries[t].input.text), assetTexts))
    orderData = data
    orderData[ORDER_NUMBER] = int(orderData[ORDER_NUMBER])
    orderData[CREATE_TIME] = int(orderData[CREATE_TIME])
    orderData[PICKUP_TIME] = int(orderData[PICKUP_TIME])
    orderData[DELIVERY_TIME] = int(orderData[DELIVERY_TIME])
    orderData[SHIPPING_PRICE] = int(orderData[SHIPPING_PRICE])
    orderData[QUANTITY] = int(orderData[QUANTITY])
    orderData[MAX_TEMPERATURE] = int(orderData[MAX_TEMPERATURE])
    orderData[MIN_TEMPERATURE] = int(orderData[MIN_TEMPERATURE])
    orderData[TOLERANCE_TIME] = int(orderData[TOLERANCE_TIME])
    orderData[MEASURE_INTERVAL] = int(orderData[MEASURE_INTERVAL])
    orderData[PENALTY_PERDAY] = float(orderData[PENALTY_PERDAY])
    orderData[MAX_PENALTY] = float(orderData[MAX_PENALTY])
    orderData[BC_SYNC_INTERVAL] = int(orderData[BC_SYNC_INTERVAL])

    bcAsset.buildAsset(orderData[ORDER_NUMBER], orderData[CREATE_TIME], orderData[PICKUP_TIME], orderData[DELIVERY_TIME], orderData[SHIPPING_PRICE], orderData[QUANTITY], orderData[MAX_TEMPERATURE], orderData[MIN_TEMPERATURE], orderData[TOLERANCE_TIME], orderData[MEASURE_INTERVAL], orderData[PENALTY_PERDAY], orderData[MAX_PENALTY], orderData[BC_SYNC_INTERVAL], orderData[INCOTERM])

    myweb3.createOrder(orderData[ORDER_NUMBER], orderData[SHIPPING_PRICE])

    popup = Popup(title='Info', content=Label(text='Submitted'), size_hint=(0.5, 0.5), font_size = 50)
    popup.open()


def getBalance(instance):
    consumerBalance = int(round(myweb3.getConsumerBalance() / 1e18))
    logisticBalance = int(round(myweb3.getLogisticBalance() / 1e18))
    contractBalance = int(round(myweb3.getContractBalance() / 1e18))
    popup = Popup(title='Info', content=Label(text='Consumer Balance: {} ether\nLogistic Balance: {} ether\nContract Balance: {} ether'.format(consumerBalance, logisticBalance, contractBalance), font_size = 50), size_hint=(0.5, 0.5))
    popup.open()


class BalanceScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(BalanceScreen, self).__init__(*args, **kwargs)
        btn = Button(text='Get Balance', size_hint=(0.2, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size = 50)
        self.add_widget(btn)
        btn.bind(on_press=getBalance)


class FormEntry(GridLayout):

    def __init__(self, name=None, *args, **kwargs):
        super(FormEntry, self).__init__(*args, **kwargs)
        self.cols = 2
        self.add_widget(Label(text=name, font_size = 50))
        self.input = TextInput(multiline=False, font_size = 50)
        self.add_widget(self.input)


class SubmitButton(Button):

    def __init__(self, father=None, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.font_size = 50
        self.text = 'Submit'
        self.father = father


class OrderLayout(GridLayout):

    def __init__(self, *args, **kwargs):
        super(OrderLayout, self).__init__(*args, **kwargs)
        self.cols = 1
        self.size_hint = (0.5, 0.95)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.spacing = 5

        self.entries = dict()

        for text in assetTexts:
            entry = FormEntry(name=text)
            self.entries[text] = entry
            self.add_widget(entry)

        self.entries[ORDER_NUMBER].input.text = '0'
        self.entries[CREATE_TIME].input.text = '1518652801'
        self.entries[PICKUP_TIME].input.text = '1518652801'
        self.entries[DELIVERY_TIME].input.text = '1518825601'
        self.entries[SHIPPING_PRICE].input.text = '10000000000000000000'
        self.entries[QUANTITY].input.text = '24'
        self.entries[MAX_TEMPERATURE].input.text = '40'
        self.entries[MIN_TEMPERATURE].input.text = '5'
        self.entries[TOLERANCE_TIME].input.text = str(45 * 60)
        self.entries[MEASURE_INTERVAL].input.text = '60'
        self.entries[PENALTY_PERDAY].input.text = '0.1'
        self.entries[MAX_PENALTY].input.text = '0.5'
        self.entries[BC_SYNC_INTERVAL].input.text = '1800'
        self.entries[INCOTERM].input.text = 'CPT'

        btn = SubmitButton(text='Submit!', father=self)
        self.add_widget(btn)
        btn.bind(on_press=submit)


class OrderScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(OrderScreen, self).__init__(*args, **kwargs)
        self.add_widget(OrderLayout())


class SensorFileChooser(FileChooserListView):

    def __init__(self, *args, **kwargs):
        super(SensorFileChooser, self).__init__(*args, **kwargs)
        self.path = 'cases'

    def on_submit(*args):
        filePath = args[1][0]
        f = open(filePath)
        lines = f.readlines()
        for line in lines:
            index, tempSensor1, tempSensor2, tempSensor3, timestamp = list(map(lambda item: int(item), line.strip('\r\n').split(',')))
            bcAsset.buildEvent(tempSensor1, tempSensor2, tempSensor3, timestamp)
        f.close()
        popup = Popup(title='Info', content=Label(text='Arrived!', font_size = 50), size_hint=(0.5, 0.5))
        popup.open()


class SensorScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(SensorScreen, self).__init__(*args, **kwargs)
        self.fileChooser = SensorFileChooser()
        self.add_widget(self.fileChooser)


def check(instance):
    global payBack, payToDelivery
    minTemperature = orderData[MIN_TEMPERATURE]
    maxTemperature = orderData[MAX_TEMPERATURE]
    events = bcAsset.getEvents()
    lastEvent = None
    events = sorted(events, key = lambda e : e['content']['data']['created_at'])
    for event in events:
        if lastEvent != None:
            lastTempSensor1 = lastEvent['content']['data']['custom']['tempSensor1']
            lastTempSensor2 = lastEvent['content']['data']['custom']['tempSensor2']
            lastTempSensor3 = lastEvent['content']['data']['custom']['tempSensor3']
            nowTempSensor1 = event['content']['data']['custom']['tempSensor1']
            nowTempSensor2 = event['content']['data']['custom']['tempSensor2']
            nowTempSensor3 = event['content']['data']['custom']['tempSensor3']
            if (not (minTemperature<=lastTempSensor1<=maxTemperature) and not (minTemperature<=nowTempSensor1<=maxTemperature)) or (not (minTemperature<=lastTempSensor2<=maxTemperature) and not (minTemperature<=nowTempSensor2<=maxTemperature)) or (not (minTemperature<=lastTempSensor3<=maxTemperature) and not (minTemperature<=nowTempSensor3<=maxTemperature)):
                payBack = orderData[SHIPPING_PRICE]
                payToDelivery = 0
                print('1')
                print('payBack {}'.format(payBack))
                print('payToDelivery {}'.format(payToDelivery))
                break
        lastEvent = event
    else:
        startEvent = events[0]
        endEvent = events[-1]
        timeSpentMore = endEvent['content']['data']['created_at'] - orderData[DELIVERY_TIME]
        daysSpentMore = ceil(timeSpentMore / (60 * 60 * 24))
        penalty = min(orderData[PENALTY_PERDAY] * daysSpentMore, orderData[MAX_PENALTY])
        payBack = int(orderData[SHIPPING_PRICE] * penalty)
        payToDelivery = orderData[SHIPPING_PRICE] - payBack
        print('2')
        print('daySpentMore {}'.format(daysSpentMore))
        print('payBack {}'.format(payBack))
        print('payToDelivery {}'.format(payToDelivery))

    popup = Popup(title='Info', content=Label(text='Pay Back: {} ether\nPay For Delivery: {} ether'.format(int(round(payBack/1e18)), int(round(payToDelivery/1e18))), font_size = 50), size_hint=(0.5, 0.5))
    popup.open()


def confirm(instance):
    myweb3.confirm(orderData[ORDER_NUMBER], payToDelivery)
    popup = Popup(title='Info', content=Label(text='Confirmed!'.format(payBack, payToDelivery), font_size = 50), size_hint=(0.5, 0.5))
    popup.open()


class ReceiveButtonsLayout(BoxLayout):

    def __init__(self, father=None, *args, **kwargs):
        super(ReceiveButtonsLayout, self).__init__(*args, **kwargs)
        self.orientation = 'horizontal'
        self.spacing = 100

        checkBtn = Button(text='Check', font_size = 50)
        checkBtn.bind(on_press=check)
        self.add_widget(checkBtn)

        confirmBtn = Button(text='Confirm', font_size = 50)
        confirmBtn.bind(on_press=confirm)
        self.add_widget(confirmBtn)

        self.father = father


class ReceiveLayout(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(ReceiveLayout, self).__init__(*args, **kwargs)
        self.orientation = 'vertical'
        self.size_hint = (0.5, 0.1)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.spacing = 200
        self.buttonLayout = ReceiveButtonsLayout(father=self)
        self.add_widget(self.buttonLayout)


class ReceiveScreen(Screen):

    def __init__(self, *args, **kwargs):
        super(ReceiveScreen, self).__init__(*args, **kwargs)
        self.add_widget(ReceiveLayout())


class Manager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(Manager, self).__init__(*args, **kwargs)
        balanceScreen = BalanceScreen(name=BALANCE)
        self.add_widget(balanceScreen)
        orderScreen = OrderScreen(name=ORDER)
        self.add_widget(orderScreen)
        sensorScreen = SensorScreen(name=SENSOR)
        self.add_widget(sensorScreen)
        receiveScreen = ReceiveScreen(name=RECEIVE)
        self.add_widget(receiveScreen)


class Navigation(GridLayout):

    def __init__(self, manager=None, *args, **kwargs):
        super(Navigation, self).__init__(*args, **kwargs)
        self.manager = manager
        self.cols = 4
        self.size_hint = (1, .1)
        for text in screenTexts:
            self.add_widget(Button(text=text, on_release=self.change, font_size = 50))


    def change(self, btn):
        self.manager.current = btn.text


class Root(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(Root, self).__init__(*args, **kwargs)
        self.orientation = 'vertical'
        manager = Manager()
        self.add_widget(Navigation(manager))
        self.add_widget(manager)


class AmBrosApp(App):

    def build(App):
        return Root()


if __name__ == '__main__':
    AmBrosApp().run()
