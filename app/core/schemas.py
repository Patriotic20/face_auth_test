from typing import Optional
from pydantic import BaseModel, Field

class Pagination(BaseModel):
    page: int = Field(1, gt=0, description="Page number, must be > 0")
    limit: int = Field(
        20,
        gt=0,
        le=100,  # maximum allowed limit
        description="Number of items per page, must be > 0 and <= 100"
    )
    search: Optional[str] = Field(None, description="Optional search query")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit

class TokenPayload(BaseModel):
    user_id: int