from pydantic import BaseModel, EmailStr
class RoomRegisterRequest(BaseModel):
    creator_name: str
    partner_name: str
    creator_email: EmailStr
    partner_email: EmailStr
    phone_number: str

class RoomLoginRequest(BaseModel):
    email: EmailStr
    secret_key: str