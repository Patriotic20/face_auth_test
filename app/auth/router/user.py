from fastapi import APIRouter, Depends
from schemas.user import UserCreate, UserCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from services.user import UserService
from core.schemas import TokenPayload, Pagination

router = APIRouter()


def get_user_service(session: AsyncSession = Depends()):
    return UserService(session=session)


async def register(
    create_data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.register(credentials=create_data)

async def login(
    login_data: UserCredentials,
    service: UserService = Depends(get_user_service),
):
    return await service.login(credentials=login_data)

async def profile(
    current_user: TokenPayload,
    service: UserService = Depends(get_user_service), 
):
    return await service.profile(user_id=current_user.user_id)

async def get_all_user(
    current_user: TokenPayload,
    pagination: Pagination,
    service: UserService = Depends(get_user_service), 
):
    pass

async def update(
    user_id: int,
    current_user: TokenPayload,
    service: UserService = Depends(get_user_service),
):
    pass

async def delete():
    pass