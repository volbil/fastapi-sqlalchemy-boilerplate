from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from datetime import datetime
from ..base import Base


class User(Base):
    __tablename__ = "service_users"

    username: Mapped[str] = mapped_column(String(16), index=True, nullable=True)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=True)
    role: Mapped[str] = mapped_column(String(64), index=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=True)
    activated: Mapped[bool] = mapped_column(default=False)
    banned: Mapped[bool] = mapped_column(default=False)

    activation_token: Mapped[str] = mapped_column(String(64), nullable=True)
    activation_expire: Mapped[datetime] = mapped_column(nullable=True)

    password_reset_token: Mapped[str] = mapped_column(String(64), nullable=True)
    password_reset_expire: Mapped[datetime] = mapped_column(nullable=True)

    last_active: Mapped[datetime]
    created: Mapped[datetime]
    login: Mapped[datetime]

    email_messages: Mapped[list["EmailMessage"]] = relationship(
        back_populates="user",
    )

    auth_tokens: Mapped[list["AuthToken"]] = relationship(
        back_populates="user",
    )

    oauth_providers: Mapped[list["UserOAuth"]] = relationship(
        foreign_keys="[UserOAuth.user_id]",
        back_populates="user",
    )
