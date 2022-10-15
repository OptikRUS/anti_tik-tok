import datetime
from typing import Optional

import ormar

from database_config import MainMeta
from users.models import User


class Video(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=120)
    description: str = ormar.String(max_length=500)
    file: str = ormar.String(max_length=1000)
    created_at: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    user: Optional[User] = ormar.ForeignKey(User)
