from fastapi import APIRouter,status,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate,UserResponse, UserUpdate
from app.db.database import get_db
from app.services.user_service import create_user, get_users, get_user, update_user, delete_user
from app.core.oauth2 import get_current_user, get_admin_user
from typing import List

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=UserResponse)
async def create_db_user(user:UserCreate,db:AsyncSession=Depends(get_db)):
    return await create_user(db,user)



@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db), current_user=Depends(get_admin_user)):
    return await get_users(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_single_user(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await get_user(db, id)

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def put_user(id: int, user: UserUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await update_user(db, id, user)

@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def patch_user(id: int, user: UserUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await update_user(db, id, user)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_single_user(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await delete_user(db, id)