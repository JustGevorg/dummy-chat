from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from managers import ConnectionManager

app = FastAPI()
connection_manager = ConnectionManager()

html = ""
with open("index.html", "r") as f:
    html = f.read()

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id):
    await connection_manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await connection_manager.broadcast(f"Client {client_id}: {data}")
