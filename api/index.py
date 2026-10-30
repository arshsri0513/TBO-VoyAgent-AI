from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI(title="VoyAgent AI API", description="TBO.com VoyageHack 4.0")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_path = os.path.join(os.path.dirname(__file__), "..", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>VoyAgent AI — TBO VoyageHack 4.0</h1>"

@app.get("/api/health")
async def health():
    return {"status": "ok", "project": "TBO-VoyAgent-AI", "version": "1.0.0"}
