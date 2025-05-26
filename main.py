from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .controllers import socketEndpoint
from .utils.ConnectionManager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(socketEndpoint.router, prefix="/ws")


@app.get("/")
async def root():
    return FileResponse("static/index.html")
