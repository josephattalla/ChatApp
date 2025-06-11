from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# from .controllers import socketEndpoint
from .controllers import Ws
from .controllers import Login
from .controllers import Register
from .controllers import Session

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(Ws.router, prefix="/ws")
app.include_router(Login.router, prefix="/api")
app.include_router(Register.router, prefix="/api")
app.include_router(Session.router, prefix="/api")


@app.get("/")
async def root():
    return FileResponse("static/index.html")
