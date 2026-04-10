from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from authentication.auth import hash_password, verify_password, create_token, get_current_user
from schemas import UserCreate, UserLogin,TokenResponse, UserResponse

router = APIRouter()

@router.post("/signup",response_model=UserResponse)
def signup(user:UserCreate,db:Session=Depends(get_db)):
    existed_user=db.query(User).filter(User.email==user.email).first()
    if existed_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password=hash_password(user.password)
    new_user=User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login",response_model=TokenResponse)
def login(user:UserLogin,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    token=create_token({"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}