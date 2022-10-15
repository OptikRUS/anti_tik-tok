import os

from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from .schemas import GetVideo, GetVideoList
from .models import Video
from .services import save_video, open_file
from users.models import User

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory="templates")

video_router = APIRouter()


@video_router.post("/upload", status_code=201, response_model=GetVideo)
async def create_video(
        back_task: BackgroundTasks,
        title: str = Form(...),
        description: str = Form(...),
        upload_video_file: UploadFile = File(...),
):
    user = await User.objects.first()
    return await save_video(user, title, description, upload_video_file, back_task)


@video_router.get("/user/{user_pk}", response_model=list[GetVideoList])
async def get_list_video(user_pk: int):
    return await Video.objects.filter(user=user_pk).all()


@video_router.get("/index/{video_pk}", response_class=HTMLResponse)
async def get_video(request: Request, video_pk: int):
    return templates.TemplateResponse("index.html", {"request": request, "path": video_pk})


@video_router.get("/video/{video_pk}", response_class=HTMLResponse)
async def get_video(request: Request, video_pk: int) -> StreamingResponse:
    file_, status_code, content_length, headers = await open_file(request, video_pk)
    response = StreamingResponse(
        file_,
        media_type="video/mov",
        status_code=status_code
    )

    response.headers.update(
        {
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            **headers,
        }
    )
    return response


@video_router.get("/404", response_class=HTMLResponse)
async def error_404(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})
