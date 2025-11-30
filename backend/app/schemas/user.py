from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """Schema para criação de utilizador"""
    username: str = Field(..., min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    """Schema para início de sessão"""
    username: str
    password: str

class UserResponse(BaseModel):
    """Schema de resposta do utilizador"""
    id: int
    username: str
    email: str
    created_at: str
    
    class Config:
        from_attributes = True

