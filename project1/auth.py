from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from project1.database import get_db
from project1.models import User
from sqlalchemy.orm import Session

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def hash_password(password:str)-> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_token (data:dict):
    to_encode = data.copy()
    expire= datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:                                                    
         payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         user_id=payload.get("user_id")
         
         if user_id is None:
             raise HTTPException(status_code=401, detail="Invalid token")
         
         db_user=db.query(User).filter(User.id==user_id).first()
         return db_user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
         
    
       
    
    