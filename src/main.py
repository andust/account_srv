from fastapi import FastAPI
from src.authentication.entrypoints import authentication
from src.authentication.adapters import orm as authentication_orm

app = FastAPI()

authentication_orm.start_mappers()

@app.get("/")
async def read_root():
    return "Ping"


API_VERSION = 1
PREFIX = f"/api/v{API_VERSION}"

app.include_router(authentication.router, prefix=f"{PREFIX}/auth")
