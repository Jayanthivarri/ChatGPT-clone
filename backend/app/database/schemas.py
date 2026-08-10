from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class SessionCreate(BaseModel):
    title: str


class SessionResponse(BaseModel):
    id: int
    title: str
    user_id: int

class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str

class Config:
    from_attributes = True

class ChatRequest(BaseModel):
    session_id: int |None=None
    message: str

class ChatResponse(BaseModel):
    session_id: int
    response: str
    tool: list[str] |None=None

class FeedbackCreate(BaseModel):
    message_id: int
    rating: str
    comment: str | None = None


class FeedbackResponse(BaseModel):
    id: int
    message_id: int
    rating: str
    comment: str | None = None

class Config:
    from_attributes = True
