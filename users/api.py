from fastapi import APIRouter

from videos.models import Video
from videos.schemas import GetVideoList

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/{user_pk}", response_model=list[GetVideoList])
async def get_list_video(user_pk: int):
    return await Video.objects.filter(user=user_pk).all()
