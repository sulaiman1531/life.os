from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, tasks, notes, habits, chat, planner, finance, projects, goals, health, learning, settings, reminders, emails, workspace
import models
from database import engine
from notifications import manager, make_notification

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LIFE OS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(notes.router, prefix="/api/notes", tags=["notes"])
app.include_router(habits.router, prefix="/api/habits", tags=["habits"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(planner.router, prefix="/api/planner", tags=["planner"])
app.include_router(finance.router, prefix="/api/finance", tags=["finance"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(goals.router, prefix="/api/goals", tags=["goals"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(learning.router, prefix="/api/learning", tags=["learning"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["reminders"])
app.include_router(emails.router, prefix="/api/emails", tags=["emails"])
app.include_router(workspace.router, prefix="/api/workspace", tags=["workspace"])

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        # Send welcome notification on connect
        await manager.send_notification(user_id, make_notification(
            type="info",
            title="LIFE OS Connected",
            message="Real-time sync is active.",
            icon="zap"
        ))
        while True:
            # Keep the connection alive — receive any client pings
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "LIFE OS Backend is running"}

