from fastapi import APIRouter, HTTPException
from models.room import RoomRegisterRequest, RoomLoginRequest
from database.mongo import rooms_collection
from utils.security import (
    generate_secret_key,
    hash_secret_key,
    verify_secret_key,
    create_jwt_token
)
from utils.email import send_secret_key_email
from datetime import datetime
import secrets

router = APIRouter(prefix="/rooms", tags=["Rooms"])

# -------------------------------
# ROOM REGISTRATION (ONE TIME)
# -------------------------------
@router.post("/register")
def register_room(data: RoomRegisterRequest):

    email1 = data.creator_email.lower()
    email2 = data.partner_email.lower()

    existing = rooms_collection.find_one({
        "$or": [
            {"creator_email": email1},
            {"partner_email": email1},
            {"creator_email": email2},
            {"partner_email": email2},
        ]
    })

    if existing:
        raise HTTPException(status_code=400, detail="Room already exists for this email")

    secret_key = generate_secret_key()
    secret_key_hash = hash_secret_key(secret_key)

    room_id = f"ROOM_{secrets.token_hex(8)}"

    rooms_collection.insert_one({
        "room_id": room_id,
        "creator_name": data.creator_name,
        "partner_name": data.partner_name,
        "creator_email": email1,
        "partner_email": email2,
        "phone_number": data.phone_number,
        "secret_key_hash": secret_key_hash,
        "created_at": datetime.utcnow(),
        "is_active": True,
        "failed_attempts": 0
    })

    send_secret_key_email(email1, secret_key)
    send_secret_key_email(email2, secret_key)

    return {"message": "Room created successfully. Check your emails for the secret key."}


# -------------------------------
# ROOM LOGIN
# -------------------------------
@router.post("/login")
def login_room(data: RoomLoginRequest):

    email = data.email.lower()

    room = rooms_collection.find_one({
        "$or": [
            {"creator_email": email},
            {"partner_email": email}
        ]
    })

    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    if not verify_secret_key(data.secret_key, room["secret_key_hash"]):
        raise HTTPException(status_code=401, detail="Invalid secret key")

    token = create_jwt_token({
        "room_id": room["room_id"],
        "email": email
    })

    return {
        "access_token": token,
        "room_id": room["room_id"]
    }
