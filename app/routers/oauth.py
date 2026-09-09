from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.core import oauth2
from app.core.utils import verify_passwords
from app.db.database import get_db
from sqlalchemy import select

router = APIRouter(tags=['Authentication'])

@router.post("/login")
async def login_user(
    user_credentials:OAuth2PasswordRequestForm=Depends(),
    db:Session=Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == user_credentials.username))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid Credentials'
        )
    
    if not verify_passwords(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid Credentials'
        )
    
    access_token = oauth2.create_access_token(data={'user_id':user.id})
    return {
        'access_token':access_token,
        'token_type':'Bearer'
    }
        