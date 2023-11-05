from app.dependencies import auth_required
from fastapi import APIRouter, Depends
from app.models import User
from app import constants


router = APIRouter(prefix="/permission", tags=["Permission"])


@router.get("/example", summary="Example permission")
async def example(
    user: User = Depends(
        auth_required(permissions=[constants.PERMISSION_EXAMPLE])
    ),
):
    return user
