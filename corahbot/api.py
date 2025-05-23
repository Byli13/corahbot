"""
REST API for remote control of the CorahBot
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import threading
import uvicorn
from corahbot.config import API_HOST, API_PORT
from corahbot.logger import get_logger
from corahbot.main import CorahBot

log = get_logger(__name__)

app = FastAPI(
    title="CorahBot API",
    description="REST API for controlling the Corah IDLE RPG bot",
    version="1.0.0"
)

# Store bot instance
bot_instance: Optional[CorahBot] = None
bot_thread: Optional[threading.Thread] = None

class CommandRequest(BaseModel):
    """Model for bot control commands"""
    command: str

class StatusResponse(BaseModel):
    """Model for bot status response"""
    status: str
    running: bool
    uptime: Optional[float] = None

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get the current status of the bot"""
    global bot_instance
    
    if bot_instance is None:
        return StatusResponse(
            status="not_initialized",
            running=False
        )
    
    return StatusResponse(
        status="running" if bot_instance.running else "stopped",
        running=bot_instance.running
    )

@app.post("/command")
async def send_command(cmd: CommandRequest):
    """Send a command to control the bot"""
    global bot_instance, bot_thread
    
    if cmd.command == "start":
        if bot_instance and bot_instance.running:
            raise HTTPException(status_code=400, detail="Bot is already running")
            
        try:
            bot_instance = CorahBot()
            bot_thread = threading.Thread(target=bot_instance.start)
            bot_thread.daemon = True  # Allow the thread to be terminated when the main process exits
            bot_thread.start()
            return {"message": "Bot started successfully"}
        except Exception as e:
            log.exception("Failed to start bot")
            raise HTTPException(status_code=500, detail=str(e))
            
    elif cmd.command == "stop":
        if not bot_instance or not bot_instance.running:
            raise HTTPException(status_code=400, detail="Bot is not running")
            
        try:
            bot_instance.stop()
            if bot_thread:
                bot_thread.join(timeout=5.0)  # Wait up to 5 seconds for the thread to finish
            return {"message": "Bot stopped successfully"}
        except Exception as e:
            log.exception("Failed to stop bot")
            raise HTTPException(status_code=500, detail=str(e))
            
    else:
        raise HTTPException(status_code=400, detail=f"Unknown command: {cmd.command}")

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy"}

def start_api():
    """Start the FastAPI server"""
    try:
        log.info(f"Starting API server on {API_HOST}:{API_PORT}")
        uvicorn.run(app, host=API_HOST, port=API_PORT)
    except Exception as e:
        log.exception("Failed to start API server")
        raise

if __name__ == "__main__":
    start_api()
