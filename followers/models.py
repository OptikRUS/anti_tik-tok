from typing import Optional

import ormar
from database_config import MainMeta

from users.models import User


class Follower(ormar.Model):
    class Meta(MainMeta):
        pass

    id: int = ormar.Integer(primary_key=True)
    user: Optional[User] = ormar.ForeignKey(User, related_name="user")
    subscriber: Optional[User] = ormar.ForeignKey(User, related_name="subscriber")

