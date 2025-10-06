from fastapi import APIRouter, Depends, HTTPException, status, Body, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from applications.user.models import User, TemporaryOTP
from app.token import create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM, REFRESH_SECRET_KEY
from app.token import get_current_user
import random
import re
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def detect_input_type(value: str) -> str:
    value = value.strip()

    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    phone_regex = r'^(\+?\d{1,4}[\s-]?)?\d{10,14}$'

    if re.match(email_regex, value):
        return 'email'
    elif re.match(phone_regex, value):
        return 'phone'
    else:
        return 'username'


@router.post("/login_auth2/")
async def loginAuth2(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }



@router.post("/login/")
async def login(
    user_key: str = Form(...),
    password: str = Form(...)
):
    lookup_field = await detect_input_type(user_key)
    
    if lookup_field == "email":
        user = await User.get_or_none(email=user_key)
    elif lookup_field == "phone":
        user = await User.get_or_none(phone=user_key)
    else:
        user = await User.get_or_none(username=user_key)


    # Try to find user
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Prepare token data
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser
    }

    # Generate tokens
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/signup/")
async def signup(
    user_key: str = Form(...),
    password: str = Form(...)
):
    lookup_field = await detect_input_type(user_key)
    
    if lookup_field == "email":
        user = await User.get_or_none(email=user_key)
    elif lookup_field == "phone":
        user = await User.get_or_none(phone=user_key)
    else: 
        raise HTTPException(
            status_code=400,
            detail=f"{lookup_field.capitalize()} is not valid"
        )

    if user:
        raise HTTPException(
            status_code=400,
            detail=f"{lookup_field.capitalize()} already registered"
        )
    
    hashed_password = pwd_context.hash(password)
    user = await User.create(
        **{lookup_field: user_key},
        password=hashed_password
    )

    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "message": "User created successfully",
        "id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/reset_password/")
async def forgot_password(
    user_key: str = Form(...),
    password: str = Form(...)
):
    lookup_field = await detect_input_type(user_key)
    
    if lookup_field == "email":
        user = await User.get_or_none(email=user_key)
    elif lookup_field == "phone":
        user = await User.get_or_none(phone=user_key)
    else: 
        user = await User.get_or_none(username=user_key)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = pwd_context.hash(password)
    await user.save()
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "message": "Password reset token created",
        "id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }



@router.get("/verify-token/")
async def verify_token(request: Request, user: User = Depends(get_current_user)):
    response_data = {
        "status": "success",
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    }

    if hasattr(request.state, "new_tokens"):
        response_data["new_tokens"] = request.state.new_tokens

    return response_data



@router.post("/send_otp/")
async def send_otp(
    user_key: str = Form(...),
    purpose: str = Form(...),
):
    otp = str(random.randint(100000, 999999))
    key_type = await detect_input_type(user_key)

    # Check user existence
    if key_type == "email":
        user = await User.get_or_none(email=user_key)
    elif key_type == "phone":
        user = await User.get_or_none(phone=user_key)
    else:  # username
        user = await User.get_or_none(username=user_key)
        
    print("user :", user)

    # Purpose-specific logic
    if purpose == "reset_password":
        if not user:
            raise HTTPException(status_code=400, detail="User not found for password reset.")

    elif purpose == "signup":
        if user:
            raise HTTPException(status_code=400, detail=f"{key_type} already registered.")

    else:
        raise HTTPException(status_code=400, detail="Invalid purpose.")

    # Store or update OTP
    existing = await TemporaryOTP.get_or_none(user_key=user_key)
    if existing:
        existing.otp = otp
        existing.created_at = datetime.now(timezone.utc)
        await existing.save()
    else:
        await TemporaryOTP.create(user_key=user_key, otp=otp)

    # TODO: integrate with email/SMS service
    print(f"OTP for {user_key}: {otp}")

    return {
        "status": "success",
        "message": f"OTP sent to {user_key}. Expires in 1 minute.",
        "purpose": purpose,
    }


@router.post("/verify_otp/")
async def verify_otp(
    user_key: str = Form(...),
    otpValue: str = Form(...)
):
    temporary = await TemporaryOTP.get_or_none(user_key=user_key)
    if not temporary:
        raise HTTPException(status_code=400, detail="No OTP found.")

    if temporary.otp != otpValue:
        raise HTTPException(status_code=400, detail="Incorrect OTP.")

    if not temporary.is_valid:
        await temporary.delete()
        raise HTTPException(status_code=400, detail="OTP has expired.")

    # OTP is correct → cleanup
    await temporary.delete()

    return {
        "status": "success",
        "message": "OTP verified successfully."
    }