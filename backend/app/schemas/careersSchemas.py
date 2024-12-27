from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from typing import List
from fastapi import UploadFile


class CareerUserCreate(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    resume_file: str

    class Config:
        from_attributes = True


class CareerUserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    mobile: Optional[str]
    is_active: Optional[bool]
    resume_file: Optional[UploadFile]

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
