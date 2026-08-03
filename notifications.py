from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            try:
                self.active_connections[user_id].remove(websocket)
            except ValueError:
                pass

    async def send_notification(self, user_id: str, notification: dict):
        if user_id in self.active_connections:
            dead = []
            for ws in self.active_connections[user_id]:
                try:
                    await ws.send_text(json.dumps(notification))
                except Exception:
                    dead.append(ws)
            for ws in dead:
                self.disconnect(ws, user_id)

    async def broadcast_to_all(self, notification: dict):
        for user_id in list(self.active_connections.keys()):
            await self.send_notification(user_id, notification)

manager = ConnectionManager()

def make_notification(type: str, title: str, message: str, icon: str = "bell") -> dict:
    return {
        "id": str(datetime.utcnow().timestamp()),
        "type": type,
        "title": title,
        "message": message,
        "icon": icon,
        "timestamp": datetime.utcnow().isoformat(),
        "read": False,
    }
