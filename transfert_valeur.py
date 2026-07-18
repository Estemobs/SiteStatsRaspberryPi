import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import db
from config import settings

BASE_DIR = os.path.dirname(__file__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=BASE_DIR)

app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, "assets")), name="assets")
app.mount("/img", StaticFiles(directory=os.path.join(BASE_DIR, "img")), name="img")
app.mount("/vues", StaticFiles(directory=os.path.join(BASE_DIR, "vues")), name="vues")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    data = db.get_latest()
    temp, cpu, ram, wifi = data if data else (None, None, None, None)
    return templates.TemplateResponse(
        "adminPI.html",
        {"request": request, "temp": temp, "proc": cpu, "ram": ram, "wifi": wifi},
    )


@app.post("/api/measurements")
def create_measurement(payload: dict, authorization: str = Header(default="")):
    if not settings.api_token:
        raise HTTPException(status_code=503, detail="API_TOKEN n'est pas configuré côté serveur")
    if authorization != f"Bearer {settings.api_token}":
        raise HTTPException(status_code=401, detail="Jeton invalide")

    required_fields = {"temperature", "cpu_usage", "ram_usage", "ping_time"}
    missing = required_fields - payload.keys()
    if missing:
        raise HTTPException(status_code=422, detail=f"Champs manquants: {', '.join(missing)}")

    db.insert_measurement(
        payload["temperature"], payload["cpu_usage"], payload["ram_usage"], payload["ping_time"]
    )
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    print(f"Listening on {settings.host}:{settings.port}")
    uvicorn.run(app, host=settings.host, port=settings.port)
