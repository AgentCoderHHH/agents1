from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
import asyncio
import json
from typing import Dict, List
from datetime import datetime
import psutil
import os
from .monitoring import MonitoringServer
from .performance import PerformanceOptimizer

app = FastAPI(title="Agent System Monitoring")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize monitoring components
monitoring_server = MonitoringServer()
performance_optimizer = PerformanceOptimizer()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the main monitoring dashboard."""
    metrics = monitoring_server.get_metrics()
    cache_stats = performance_optimizer.get_cache_stats()
    system_stats = get_system_stats()
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "metrics": metrics,
            "cache_stats": cache_stats,
            "system_stats": system_stats
        }
    )

@app.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics updates."""
    await websocket.accept()
    
    try:
        while True:
            metrics = monitoring_server.get_metrics()
            system_stats = get_system_stats()
            
            await websocket.send_json({
                "metrics": metrics,
                "system_stats": system_stats,
                "timestamp": datetime.now().isoformat()
            })
            
            await asyncio.sleep(1)  # Update every second
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

@app.get("/api/metrics")
async def get_metrics():
    """API endpoint for current metrics."""
    return {
        "metrics": monitoring_server.get_metrics(),
        "cache_stats": performance_optimizer.get_cache_stats(),
        "system_stats": get_system_stats(),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/performance")
async def get_performance():
    """API endpoint for performance statistics."""
    return {
        "cache_stats": performance_optimizer.get_cache_stats(),
        "system_stats": get_system_stats()
    }

def get_system_stats() -> Dict[str, float]:
    """Get current system statistics."""
    process = psutil.Process(os.getpid())
    
    return {
        "cpu_percent": process.cpu_percent(),
        "memory_percent": process.memory_percent(),
        "memory_used": process.memory_info().rss / 1024 / 1024,  # MB
        "threads": process.num_threads(),
        "connections": len(process.connections())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 