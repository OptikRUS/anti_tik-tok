from fastapi import FastAPI

from database_config import database, metadata, engine
from videos.api import video_router
from users.api import users_router
from followers.api import followers_router

app = FastAPI(title="FastApi Video hosting", version='0.1.1', description="Simple video hosting")

app.state.database = database
metadata.create_all(engine)


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


app.include_router(video_router)
app.include_router(users_router)
app.include_router(followers_router)
