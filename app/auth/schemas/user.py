from pydantic import BaseModel, field_validator, field_serializer
from .role import RoleListResponse
from core.utils.normalize_str import normalize_str
from utils.password_utils import hash_password

class UserCreate(BaseModel):
    username: str
    password: str
    
    @field_validator('username', mode='before')
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return normalize_str(value)
    
    @field_validator('password', mode='before')
    @classmethod
    def validate_and_hash_password(cls, value: str) -> str:
        """Validate password rules THEN hash it"""
        value = value.strip()
                
        # Now hash the validated password
        return hash_password(password=value)
    




class UserCredentials(BaseModel):
    username: str
    password: str
    
    @field_validator('username', mode='before')
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return normalize_str(value)
    
    @field_validator('password', mode='before')
    @classmethod
    def clean_password(cls, value: str) -> str:
        """Clean password input - DO NOT hash for login"""
        return value.strip()


class UserDetailResponse(BaseModel):
    id: int
    username: str
    roles: RoleListResponse  
    
    @field_serializer('username')
    @classmethod
    def normalize(cls, value: str) -> str:
        """Normalize username for display"""
        return value.title()


class UserListItem(BaseModel):
    id: int
    username: str
    
    @field_serializer('username')
    @classmethod
    def normalize(cls, value: str) -> str:
        """Normalize username for display"""
        return value.title()


class UserListResponse(BaseModel):
    data: list[UserListItem]


class UserUpdate(BaseModel):
    username: str
    
    @field_validator('username', mode='before')
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return normalize_str(value)


class UserChangePassword(BaseModel):  
    old_password: str
    new_password: str
    
    @field_validator('*', mode='before')
    @classmethod
    def clean_old_password(cls, value: str) -> str:
        """Clean old password - DO NOT hash (needed for verification)"""
        return value.strip()


