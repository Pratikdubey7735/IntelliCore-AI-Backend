from pydantic import BaseModel, EmailStr

class SignupModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"

class LoginModel(BaseModel):
    email: EmailStr
    password: str