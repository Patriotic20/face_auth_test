from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from pydantic import BaseModel



class BaseCRUD:
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model
    
    async def create(self, create_data: BaseModel):
        new_object = self.model(**create_data.model_dump())
        self.session.add(new_object)
        await self.session.commit()
        await self.session.refresh(new_object)
        return new_object
    
    async def read(self, id: int):
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update(self, id: int, update_data: BaseModel):
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()
    
    async def delete(self, id: int):
        stmt = delete(self.model).where(self.model.id == id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True

