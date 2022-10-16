from pydantic import BaseModel

from users.schemas import User, UserResp


class FollowerCreate(BaseModel):
    user: int


class FollowerCreateResponse(BaseModel):
    user: UserResp
    subscriber: User


class FollowerList(BaseModel):
    subscriber: User


class FollowingList(BaseModel):
    user: User
