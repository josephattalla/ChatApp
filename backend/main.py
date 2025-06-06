from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .controllers import socketEndpoint
from .controllers import Login
from .utils.ConnectionManager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(socketEndpoint.router, prefix="/ws")
app.include_router(Login.router, prefix="/api")


@app.get("/")
async def root():
    return FileResponse("static/index.html")
