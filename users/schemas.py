from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str


class UserResp(BaseModel):
    username: str
