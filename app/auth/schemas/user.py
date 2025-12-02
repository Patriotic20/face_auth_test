from pydantic import BaseModel
from .role import RoleListResponse

class UserDetailResponse(BaseModel):
    id: int
    username: str
    roles: RoleListResponse  # list of roles (only id & name)


class UserListItem(BaseModel):
    id: int
    username: str

class UserListResponse(BaseModel):
    data: list[UserListItem]
