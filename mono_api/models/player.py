from fastapi import WebSocket

class Player:
    def __init__(self, name: str, websocket: WebSocket):
        self.name = name
        if(name=='bank'):
            self.cash = 999999
        else:
            self.cash = 0
        self.websocket = websocket

    def addMoney(self, cash: int):
        self.cash += cash

    def restMoney(self, cash: int):
        if(self.cash - cash < 0):
            return False

        self.cash -= cash
        return True
