from fastapi import APIRouter,status,Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.cover_letter import CoverLetterCreate,CoverLetterResponse, CoverLetterUpdate
from app.services.cover_letter_service import create_cover_letter_service,get_cover_letters_service,get_cover_letter_service, update_cover_letter_service, delete_cover_letter
from app.core.oauth2 import get_current_user, get_admin_user
from typing import List


router = APIRouter(
    prefix='/cover_letters',
    tags=['CoverLetters']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CoverLetterResponse)
def create_cover_letter(cover_letter: CoverLetterCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_cover_letter_service(db, cover_letter)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CoverLetterResponse])
def get_cover_letters(db: Session = Depends(get_db), current_user=Depends(get_admin_user)):
    return get_cover_letters_service(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CoverLetterResponse)
def get_cover_letter(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_cover_letter_service(db, id)

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=CoverLetterResponse)
def put_cover_letter(id: int, cover_letter: CoverLetterUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_cover_letter_service(db, id, cover_letter)

@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=CoverLetterResponse)
def patch_cover_letter(id: int, cover_letter: CoverLetterUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_cover_letter_service(db, id, cover_letter)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_cover_letter_endpoint(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_cover_letter(db, id)
