from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import os

app = FastAPI(title="VoyAgent AI", description="TBO.com VoyageHack 4.0")

# Load index.html
HTML_PAGE = ""
current_dir = os.path.dirname(os.path.abspath(__file__))
candidate_paths = [
    os.path.join(current_dir, "index.html"),
    os.path.join(current_dir, "..", "index.html"),
    os.path.abspath("index.html")
]

for p in candidate_paths:
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                HTML_PAGE = f.read()
                break
        except Exception:
            pass

@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "VoyAgent AI", "track": "Virtual travel Agent / copilot"}

# Catch-all route to serve the rich interactive UI on ALL paths (/, /api, /index, etc.)
@app.api_route("/{full_path:path}", methods=["GET", "POST", "HEAD"])
async def catch_all(request: Request, full_path: str = ""):
    if full_path == "api/health":
        return JSONResponse({"status": "ok", "app": "VoyAgent AI"})
    if HTML_PAGE:
        return HTMLResponse(content=HTML_PAGE, status_code=200)
    return HTMLResponse("<h1>VoyAgent AI - TBO.com VoyageHack 4.0</h1>", status_code=200)
