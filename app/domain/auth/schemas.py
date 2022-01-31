from pydantic import BaseModel


class SignupForm(BaseModel):
    username: str
    password: str


class LoginForm(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token_type: str
    access_token: str
