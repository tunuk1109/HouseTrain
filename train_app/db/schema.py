from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserProfileSchema(BaseModel):

    id: int
    first_name: str
    last_name: Optional[str]
    username: str
    email: EmailStr
    password: str
    age: Optional[int]
    phone_number: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class HouseSchema(BaseModel):

    GrLivArea: int
    YearBuilt: int
    GarageCars: int
    TotalBsmtSF: int
    FullBath: int
    OverallQual: int
    Neighborhood: Optional[str] = None
    SalePrice: Optional[int] = None

    class Config:
        from_attributes = True



















