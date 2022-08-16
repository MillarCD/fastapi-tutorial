from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import pyautogui


app = FastAPI()

KEYS = ['enter', 'backspace', 'space']
def press_keys(key: str):
    
    if (key in KEYS or len(key)==1):
        pyautogui.press(key)


@app.websocket("/keyboard")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print('[CLIENT KEY]: ', data)
            press_keys( data )
            await websocket.send_text(f'{data}')
    except WebSocketDisconnect:
        print('El cliente se desconecto')
