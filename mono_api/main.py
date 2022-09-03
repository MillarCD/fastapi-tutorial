from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from ast import literal_eval

from .models.manager import Manager 
from .models.game import Game
from .models.player import Player

app = FastAPI()

manager = Manager()
game = Game()


# ENDPOINTS

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    if not game.getPlayer('bank'):
        game.addPlayer( Player('bank', websocket) )

    try:
        while True:
            data = await websocket.receive_text()
            data = literal_eval(data)

            # identificar el contenido del mensaje
            if data['content'] == 'create':
                res, player = game.addPlayer( Player(data['name'], websocket ) )
                if res:
                    await manager.broadcast({'content': 'new_player', 'name': player.name})
                await manager.sendMsg({'content': 'create', 'name': player.name, 'money': player.money}, websocket)

            elif data['content'] == 'transfer':
                playersList = game.transfer(data['from'], data['to'], data['monto'])
                for player in playersList:
                    await manager.sendMsg({'content': 'transfer', 'name': player.name, 'money': player.money}, player.websocket)
            
    except WebSocketDisconnect:
        print('finish...')
