from pydantic import BaseModel, EmailStr


class LoginData(BaseModel):
    username: str
    password: str


class UserData(LoginData):
    firstname: str
    lastname: str
    email: EmailStr
