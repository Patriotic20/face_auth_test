from pydantic import BaseModel
from fastapi import HTTPException, status
from auth.schemas.user import UserCreate
from model.user import User
from model.role import Role
from core.schemas import Pagination
from sqlalchemy import select, func
from core.utils.normalize_str import normalize_str
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # -----------------------------------
    # CREATE
    # -----------------------------------
    async def create_user(self, create_data: UserCreate):
        try:
            new_user = User(**create_data.model_dump())
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)
            return new_user

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error creating user: {e}"
            )

    # -----------------------------------
    # LIST (pagination + search)
    # -----------------------------------
    async def list_user(self, pagination: Pagination):
        try:
            stmt = select(User)

            if pagination.search:
                search_term = f"%{normalize_str(pagination.search)}%"
                stmt = stmt.filter(User.username.ilike(search_term))

            # total count
            total_stmt = select(func.count()).select_from(stmt.subquery())
            total = (await self.session.execute(total_stmt)).scalar()

            stmt = stmt.limit(pagination.limit).offset(pagination.offset)

            result = await self.session.execute(stmt)
            users = result.scalars().all()

            return {
                "items": users,
                "total": total,
                "page": pagination.page,
                "limit": pagination.limit,
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error fetching user list: {e}"
            )

    # -----------------------------------
    # DETAIL (with roles + permissions)
    # -----------------------------------
    async def user_detail(self, user_id: int):
        try:
            stmt = (
                select(User)
                .where(User.id == user_id)
                .options(
                    selectinload(User.roles).selectinload(Role.permissions)
                )
            )

            result = await self.session.execute(stmt)
            user_data = result.scalar_one_or_none()

            if not user_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            return user_data

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error fetching user: {e}"
            )

    # -----------------------------------
    # UPDATE
    # -----------------------------------
    async def user_update(self, user_id: int, update_data: BaseModel):
        try:
            stmt = select(User).where(User.id == user_id)
            result = await self.session.execute(stmt)
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found for update"
                )

            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)

            await self.session.commit()
            await self.session.refresh(user)
            return user

        except HTTPException:
            raise

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error updating user: {e}"
            )

    # -----------------------------------
    # DELETE
    # -----------------------------------
    async def user_delete(self, user_id: int):
        try:
            stmt = select(User).where(User.id == user_id)
            result = await self.session.execute(stmt)
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found for delete"
                )

            await self.session.delete(user)
            await self.session.commit()
            return True

        except HTTPException:
            raise

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error deleting user: {e}"
            )
