from utils.password_utils import verify_password
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from repository.user import UserRepository
from schemas.user import UserCreate, UserListItem, UserCredentials, UserDetailResponse
from sqlalchemy import select
from model.user import User
from utils.jwt_tokens import create_access_token, create_refresh_token
from core.schemas import Pagination

class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = UserRepository(session=self.session)
    
    async def register(self, credentials: UserCreate):
        user_data = await self.repo.create_user(create_data=credentials)
        return UserListItem(id=user_data.id, username=user_data.username)

    async def login(self, credentials: UserCredentials):
        # Fetch user from DB
        stmt = select(User).where(User.username == credentials.username)
        result = await self.session.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Verify password
        if not verify_password(hashed_password=user.password, plain_password=credentials.password):
            raise HTTPException(  # use raise, not return
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )

        # Prepare token payload
        token_payload = {"user_id": user.id, "role": user.roles}

        # Create tokens
        return {
            "type": "Bearer",
            "access_token": create_access_token(data=token_payload),
            "refresh_token": create_refresh_token(data=token_payload),
        }


    async def profile(self, user_id: int):
        return await self.repo.user_detail(user_id=user_id)

    async def get_all_user(self, pagination: Pagination):
        return await self.repo.list_user(pagination=pagination)

    async def update_username(self):
        pass

    async def update_password(self):
        pass

    async def delete(self, user_id: int):
        pass