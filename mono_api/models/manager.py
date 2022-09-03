from fastapi import WebSocket

class Manager:
    def __init__(self):
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def sendMsg(self, data: dict, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast(self, data: dict):
        for connection in self.connections:
            await connection.send_json(data)
