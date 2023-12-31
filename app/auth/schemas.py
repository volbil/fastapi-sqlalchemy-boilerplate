from pydantic import EmailStr, Field
from app.schemas import CustomModel
from datetime import datetime


# Args
class TokenArgs(CustomModel):
    token: str = Field(examples=["CQE-CTXVFCYoUpxz_6VKrHhzHaUZv68XvxV-3AvQbnA"])


class EmailArgs(CustomModel):
    email: EmailStr = Field(examples=["user@mail.com"])


class UsernameArgs(CustomModel):
    username: str = Field(
        pattern="^[A-Za-z][A-Za-z0-9_]{4,15}$", examples=["username"]
    )


class SignupArgs(UsernameArgs):
    password: str = Field(min_length=8, max_length=64, examples=["password"])
    email: EmailStr = Field(examples=["user@mail.com"])


class LoginArgs(CustomModel):
    password: str = Field(min_length=8, max_length=64, examples=["password"])
    email: EmailStr = Field(examples=["user@mail.com"])


class ComfirmResetArgs(CustomModel):
    password: str = Field(min_length=8, max_length=64, examples=["password"])
    token: str = Field(examples=["CQE-CTXVFCYoUpxz_6VKrHhzHaUZv68XvxV-3AvQbnA"])


class CodeArgs(CustomModel):
    code: str


# Responses
class ProviderUrlResponse(CustomModel):
    url: str = Field(examples=["https://accounts.google.com/o/oauth2/v2/auth"])


class TokenResponse(CustomModel):
    expiration: datetime = Field(examples=[1686088809])
    created: datetime = Field(examples=[1686088809])
    secret: str = Field(
        examples=["CQE-CTXVFCYoUpxz_6VKrHhzHaUZv68XvxV-3AvQbnA"]
    )
