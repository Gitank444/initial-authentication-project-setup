from pydantic import BaseModel,Field

class UserCreate(BaseModel):
    username: str
    email: str
    password: str= Field(min_length=6, max_length=50)

class UserLogin(BaseModel):
    email: str
    password: str
    
class TokenResponse(BaseModel):
    access_token:str
    token_type:str="bearer"    
    
class UserResponse(BaseModel):
    id:int
    username:str
    email:str
   
    model_config = {"from_attributes": True}