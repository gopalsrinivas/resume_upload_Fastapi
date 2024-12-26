from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from typing import List


class CareerUserCreate(BaseModel):
    name: str = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="User's email")
    mobile: str = Field(..., description="User's mobile")
    resume_file: str = Field(..., description="Uploaded resume filename")

    class Config:
        from_attributes = True


class CareerUserResponse(BaseModel):
    id: int
    user_id: str
    name: str
    email: str
    mobile: str
    resume_filename: Optional[str] = None
    is_active: bool
    created_on: datetime
    updated_on: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaginatedCareerUsersResponse(BaseModel):
    total_users: int
    users: List[CareerUserResponse]

    class Config:
        from_attributes = True
