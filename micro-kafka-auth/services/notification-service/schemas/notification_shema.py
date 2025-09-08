from pydantic import BaseModel, EmailStr

class NotificationMessage(BaseModel):
    email: EmailStr
    subject: str
    body: str
