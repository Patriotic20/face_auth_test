from pydantic import BaseModel, Field, field_validator, field_serializer
from core.utils.normalize_str import normalize_str
from .permission import PermissionDetail

class RoleCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return normalize_str(value)


class RoleDetail(BaseModel):
    id: int
    name: str
    permissions: list[PermissionDetail]

    @field_serializer("name")
    @classmethod
    def format_name(cls, value: str) -> str:
        return value.title()


class RoleListItem(BaseModel):
    id: int
    name: str

    @field_serializer("name")
    @classmethod
    def format_name(cls, value: str) -> str:
        return value.title()
    

class RoleListResponse(BaseModel):
    data: list[RoleListItem]
