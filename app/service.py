from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from .models import User, AuthToken
from sqlalchemy import select


async def get_user_by_username(
    session: AsyncSession, username: str
) -> User | None:
    return await session.scalar(select(User).filter(User.username == username))


async def get_auth_token(
    session: AsyncSession, secret: str
) -> AuthToken | None:
    return await session.scalar(
        select(AuthToken)
        .filter(AuthToken.secret == secret)
        .options(selectinload(AuthToken.user))
    )
