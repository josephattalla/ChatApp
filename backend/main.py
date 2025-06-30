from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .controllers import Ws
from .controllers import Login
from .controllers import Register
from .controllers import Session
from .controllers import Rooms
from .controllers import Admin
from .controllers import Mod

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(Ws.router, prefix="/ws")
app.include_router(Login.router, prefix="/api")
app.include_router(Register.router, prefix="/api")
app.include_router(Session.router, prefix="/api")
app.include_router(Rooms.router, prefix="/api")
app.include_router(Admin.router, prefix="/api/admin")
app.include_router(Mod.router, prefix="/api/mod")


@app.get("/")
async def root():
    return FileResponse("static/index.html")
