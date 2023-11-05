from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .schemas import CustomModel
from fastapi import Request
from pydantic import Field


class ErrorResponse(CustomModel):
    message: str = Field(examples=["Example error message"])
    code: str = Field(examples=["example:error"])


errors = {
    "auth": {
        "username-required": ["Username is required to do that action", 400],
        "activation-valid": ["Previous activation token still valid", 400],
        "reset-valid": ["Previous password reset token still valid", 400],
        "email-required": ["Email is required to do that action", 400],
        "email-exists": ["User with that email already exists", 400],
        "activation-expired": ["Activation token has expired", 400],
        "activation-invalid": ["Activation token is invalid", 400],
        "oauth-code-required": ["OAuth code required", 400],
        "invalid-provider": ["Invalid OAuth provider", 400],
        "username-taken": ["Username already taken", 400],
        "reset-expired": ["Reset token has expired", 400],
        "reset-invalid": ["Reset token is invalid", 400],
        "already-activated": ["Already activated", 400],
        "invalid-token": ["Auth token is invalid", 400],
        "invalid-password": ["Invalid password", 400],
        "username-set": ["Username already set", 400],
        "not-activated": ["User not activated", 400],
        "token-expired": ["Token has expired", 400],
        "invalid-code": ["Invalid OAuth code", 400],
        "oauth-error": ["Error during OAuth", 400],
        "user-not-found": ["User not found", 404],
        "email-set": ["Email already set", 400],
        "banned": ["Banned", 403],
    },
    "permission": {
        "denied": ["You don't have permission for this action", 403],
    },
    "user": {
        "not-found": ["User not found", 404],
    },
}


class Abort(Exception):
    def __init__(self, scope: str, message: str):
        self.scope = scope
        self.message = message


def build_error_code(scope: str, message: str):
    return scope.replace("-", "_") + ":" + message.replace("-", "_")


async def abort_handler(request: Request, exception: Abort):
    error_code = build_error_code(exception.scope, exception.message)

    try:
        error_message = errors[exception.scope][exception.message][0]
        status_code = errors[exception.scope][exception.message][1]
    except Exception:
        error_message = "Unknown error"
        status_code = 400

    return JSONResponse(
        status_code=status_code,
        content={
            "message": error_message,
            "code": error_code,
        },
    )


async def validation_handler(
    request: Request, exception: RequestValidationError
):
    error_message = str(exception).replace("\n", " ").replace("   ", " ")
    return JSONResponse(
        status_code=400,
        content={
            "code": "system:validation_error",
            "message": error_message,
        },
    )
