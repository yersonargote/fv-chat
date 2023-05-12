from starlette.websockets import WebSocket, WebSocketDisconnect
from .database import SessionLocal
from .models import ChatMessage
import json

# Global variable to store the WebSocket connection
connected_websockets = set()


async def broadcast(message):
    for websocket in connected_websockets:
        await websocket.send_json(message)


async def websocket_endpoint(websocket: WebSocket):
    connected_websockets.add(websocket)
    await websocket.accept()
    try:
        while True:
            try:
                # Wait for new messages from the WebSocket
                data = await websocket.receive_text()
            except WebSocketDisconnect:
                if websocket in connected_websockets:
                    connected_websockets.remove(websocket)
                break

            # Parse the message data as a JSON object
            message = json.loads(data)

            # Create a new chat message in the database
            chat_message = ChatMessage(
                username=message["username"],
                message=message["message"],
            )
            db = SessionLocal()
            db.add(chat_message)
            db.commit()
            # Send the new chat message to all connected clients
            await broadcast({"status": "ok", "message": message})
    finally:
        if websocket in connected_websockets:
            connected_websockets.remove(websocket)


async def close_websockets():
    for websocket in connected_websockets:
        await websocket.close()
