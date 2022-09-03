from fastapi import WebSocket

class Player:
    def __init__(self, name: str, websocket: WebSocket):
        self.name = name
        if(name=='bank'):
            self.money = 999999
        else:
            self.money = 0
        self.websocket = websocket

    def addMoney(self, money: int):
        self.money += money

    def restMoney(self, money: int):
        if(self.money - money < 0):
            return False

        self.money -= money
        return True
