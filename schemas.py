import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str


class UploadVideo(BaseModel):
    title: str
    description: str


class GetVideoList(BaseModel):
    title: str
    description: str
    created_at: datetime.datetime


class GetVideo(GetVideoList):
    id: int
    user: User


class Message(BaseModel):
    message: str
