from pydantic import BaseModel
from core.base_crud import BaseCRUD
from auth.schemas.role import RoleCreate
from model.role import Role     
from core.schemas import Pagination

class RoleRepository(BaseCRUD):
    def __init__(self, session):
        super().__init__(session, Role)  # Pass model to BaseCRUD

    async def create_role(self, create_data: RoleCreate):
        # Use the base CRUD create method
        role = await super().create(create_data)
        # You can add custom logic here if needed
        # For example: logging, additional relations, etc.
        return role
    
    async def role_list(self, pagination: Pagination):
        pass
