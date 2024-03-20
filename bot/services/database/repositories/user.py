import secrets
from typing import Any, Dict, List, Optional, cast

from sqlalchemy import Result, Select, and_, func, select

from ....enums import UserStatus
from ..models import DBUser
from .base import BaseRepository


class UserRepository(BaseRepository):
    """
    The repository for the users.
    """

    async def get(self, user_id: int) -> Optional[DBUser]:
        """
        Get a user by their ID.

        :param user_id: The user's ID.
        :return: The user, if found.
        """
        return cast(
            Optional[DBUser],
            await self._session.scalar(select(DBUser).where(DBUser.id == user_id)),
        )

    async def get_random_companion(self, user_id: int) -> Optional[DBUser]:
        """
        Get a random companion for the user.

        :param user: The user's ID.
        :return: The companion's ID, if found.
        """
        query: Select[tuple[int]] = select(DBUser.id).where(
            and_(DBUser.status == UserStatus.WAITING, DBUser.id != user_id)
        )
        result: Result[tuple[int]] = await self._session.execute(query)
        companions: Optional[List[int]] = list(result.scalars().all())
        companion: Optional[int] = secrets.choice(companions) if companions else None
        return cast(Optional[DBUser], await self.get(user_id=companion))

    async def update_companions(
        self,
        user: DBUser,
        companion: DBUser,
        user_status: UserStatus,
        companion_status: UserStatus,
        is_stop: Optional[bool] = False,
    ) -> None:
        """
        Update the companions.

        :param user: The user.
        :param companion: The companion.
        :param user_status: The user's status.
        :param companion_status: The companion's status.
        :param is_stop: Whether the user stopped the conversation.
        """
        user.companion, companion.companion = (None, None) if is_stop else (companion.id, user.id)
        user.status, companion.status = user_status.value, companion_status.value

    async def top(self) -> Dict[str, Any]:
        """
        Get the top 3 users.

        :return: The top 3 users.
        """
        result: Result[tuple[str, int]] = await self._session.execute(
            select(DBUser.name, DBUser.balance).order_by(DBUser.balance.desc())
        )
        users: List[tuple[str, int]] = list(result.all())

        return {
            "first_user": users[0][0] if users else "🤖 Roboto",
            "second_user": users[1][0] if len(users) > 1 else "🤖 Roboto",
            "third_user": users[2][0] if len(users) > 2 else "🤖 Roboto",
            "first_cookie": users[0][1] if users else 0,
            "second_cookie": users[1][1] if len(users) > 1 else 0,
            "third_cookie": users[2][1] if len(users) > 2 else 0,
        }

    async def position(self, balance: int) -> int:
        """
        Get the user's position in the top.

        :param balance: The user's balance.
        :return: The user's position.
        """
        return cast(
            int,
            await self._session.scalar(select(func.count()).where(DBUser.balance > balance)) + 1,
        )

    async def all(self) -> int:
        """
        Get all users.

        :return: The users.
        """
        return await self._session.scalar(select(func.count()).select_from(DBUser))
