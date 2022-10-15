import shutil
from pathlib import Path
from typing import Generator, IO
from uuid import uuid4

import ormar
from fastapi import UploadFile, BackgroundTasks, HTTPException, Request

from .schemas import UploadVideo
from .models import Video, User


async def save_video(
        user: User,
        title: str,
        description: str,
        upload_video_file: UploadFile,
        background_tasks: BackgroundTasks
):
    file_type = upload_video_file.filename.split(".")[-1]
    file_name_path = f"media/{user.id}_{uuid4()}.{file_type}"
    if file_type == "mov":
        background_tasks.add_task(write_video, file_name_path, upload_video_file)
    else:
        raise HTTPException(status_code=418, detail=f"Format '{file_type}' is not supported")
    info = UploadVideo(title=title, description=description)

    return await Video.objects.create(file=file_name_path, user=user, **info.dict())


def write_video(file_name: str, file: UploadFile):
    # async with aiofiles.open(file_name, "wb") as buffer:
    #     data = await file.read()
    #     await buffer.write(data)
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


async def open_file(request: Request, video_pk: int) -> tuple:
    try:
        file = await Video.objects.get(pk=video_pk)
    except ormar.exceptions.NoMatch:
        raise HTTPException(status_code=404, detail="Not found")
    path = Path(file.dict().get('file'))
    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    headers = {}
    content_range = request.headers.get('range')

    if content_range is not None:
        content_range = content_range.strip().lower()
        content_ranges = content_range.split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, headers
