from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .schemas import FollowerCreate, FollowerCreateResponse, FollowerList, FollowingList
from .models import Follower

from users.models import User

followers_router = APIRouter(prefix="/followers", tags=["followers"])


@followers_router.post("/", status_code=201, response_model=FollowerCreateResponse, description='connect follow')
async def add_follower(follower: FollowerCreate):
    user = await User.objects.first()
    follower = await User.objects.get(id=follower.user)
    return await Follower.objects.create(user=user, subscriber=follower)


@followers_router.get("/", response_model=list[FollowingList], description='following list')
async def following_list():
    user = await User.objects.get(pk=2)
    return await Follower.objects.select_related("user").filter(subscriber=user).all()


@followers_router.get("/me", response_model=list[FollowerList], description='followers list')
async def followers_list():
    user = await User.objects.first()
    return await Follower.objects.select_related("subscriber").filter(user=user).all()


@followers_router.delete("/{follower_pk}", status_code=204, description='delete follower')
async def delete_follower(follower_pk: int):
    user = await User.objects.first()
    follower = await Follower.objects.get_or_none(user=user, subscriber=follower_pk)
    if follower:
        return await follower.delete()
    return JSONResponse(status_code=404, content={"detail": "This subscription does not exist"})
