# This file is to contains authentication related Pydanic types


import re
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, validator


class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    password: constr(min_length=8, max_length=20)

    @validator('password')
    def validate_password_strength(cls, passwordToValidate):
        # Regular expression for a strong password (at least 8 characters,
        # containing at least one uppercase letter, one lowercase letter, one digit, and one special character)
        strong_password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$'
        
        if not any(char.isdigit() for char in passwordToValidate):
            raise ValueError('Password must contain at least one digit')
        
        if not any(char.islower() for char in passwordToValidate):
            raise ValueError('Password must contain at least one lowercase letter')
        
        if not any(char.isupper() for char in passwordToValidate):
            raise ValueError('Password must contain at least one uppercase letter')
        
        if not any(char in '@$!%*?&' for char in passwordToValidate):
            raise ValueError('Password must contain at least one special character')
        
        if len(passwordToValidate) < 8 or len(passwordToValidate) > 20:
            raise ValueError('Password length must be between 8 and 20 characters')
        
        if not any(char.isalnum() or char in '@$!%*?&' for char in passwordToValidate):
            raise ValueError('Password can only contain letters, digits, and special characters')

        if not re.match(strong_password_regex, passwordToValidate):
            raise ValueError('Password is not strong enough')

        return passwordToValidate

class UserLogin(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    username: str
    email: EmailStr
    confirm_password: str
    
class UserCreateDb(UserCreate):
    hashed_password: str

class GetUserType(BaseModel):
    id: UUID
    email: str
    username: str
    created_at: datetime