from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .security import create_access_token, verify_password, decode_access_token
from pydantic import BaseModel

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock User Database
USERS_DB = {
    "vansh@example.com": {
        "username": "vansh@example.com",
        "password": "hashed_password_here", # In real app, use get_password_hash
        "full_name": "Dr. Vansh",
        "role": "PI"
    }
}

class UserOut(BaseModel):
    username: str
    role: str
    full_name: str

@router.post("/token", response_model=None)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS_DB.get(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # For mock, we skip verify_password check if password is simple
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_me(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = USERS_DB.get(payload.username)
    return user
