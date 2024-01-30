from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.dependencies import create_access_token, get_password_hash, verify_password
from auth.db_queries import create_user, get_user_by_email, get_user_by_username
from models.auth import Token, UserCreate, UserLogin
from dependencies import get_db
from utils import UUIDEnabledJsonEncoder as JSON

router = APIRouter(
    prefix="/auth"
)


@router.post("/signup", status_code=201, response_model=Token)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Get user details
    username = user.username
    email = user.email
    password = user.password
    confirm_password = user.confirm_password

    # Validate user details
    if not username:
        raise HTTPException(status_code=400, detail="username was not provided")
    
    if not email:
        raise HTTPException(status_code=400, detail="email was not provided")
    
    if not password == confirm_password: 
        raise HTTPException(status_code=400, detail="passwords do not match") 
    
    # check db for if username or email exists
    check = get_user_by_username(db, username)
    if check: 
        raise HTTPException(status_code=403, detail="User with username already exists")
    
    check = get_user_by_email(db, email)
    if check: 
        raise HTTPException(status_code=403, detail="User with email already exists")

    # hash password and save user
    hashed_password = get_password_hash(password)
    new_user = create_user(db, username, email, hashed_password)

    # create access tokens
    token = create_access_token({"username": new_user.username, "id": JSON().encode(new_user.id), "email": new_user.email})
    return {"access_token": token, "token_type": "Bearer"}


@router.post("/login", status_code=200, response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    username = user.username
    email = user.email
    password = user.password

    # Get user from database and throw relevant errors otherwise
    if username and username != "":
        user = get_user_by_username(db, username)
    elif email and email != "":
        user = get_user_by_email(db, email)
    else:
        raise HTTPException(status_code=400, detail="No Username or Email was passed.")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Hash password and check that it is correct
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Wrong Password")

    # Generate access token
    token = create_access_token({"username": user.username, "id": JSON().encode(user.id), "email": user.email})
    return {"access_token": token, "token_type": "Bearer"}