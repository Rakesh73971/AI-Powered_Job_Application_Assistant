from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate,UserResponse
from app.db.database import get_db
from app.services.user_service import create_user
from app.core.oauth2 import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def create_db_user(user:UserCreate,db:Session=Depends(get_db)):
    return create_user(db,user)



