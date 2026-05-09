import os
import shutil
from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.schemas.resume import ResumeResponse, ResumeUpdate
from app.db.database import get_db
from app.services.resume_service import (
    add_resume_service, get_resume_services, get_resume_service,
    delete_resume_service, get_user_resumes, update_resume_service
)
from app.core.oauth2 import get_current_user, get_admin_user
from typing import List

UPLOAD_DIR = "uploads/resumes"

router = APIRouter(
    prefix='/resumes',
    tags=['Resumes']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResumeResponse)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Validate PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted."
        )

    # Save file to disk
    user_dir = os.path.join(UPLOAD_DIR, str(current_user.id))
    os.makedirs(user_dir, exist_ok=True)
    file_path = os.path.join(user_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return add_resume_service(
        db=db,
        file_name=file.filename,
        file_path=file_path,
        user_id=current_user.id
    )


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ResumeResponse])
def get_resumes(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    role_value = current_user.role.value if hasattr(current_user.role, 'value') else current_user.role
    if role_value == "admin":
        return get_resume_services(db)
    return get_user_resumes(db, current_user.id)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ResumeResponse)
def get_resume(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_resume_service(db, id)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=ResumeResponse)
def put_resume(id: int, resume: ResumeUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_resume_service(db, id, resume)


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=ResumeResponse)
def patch_resume(id: int, resume: ResumeUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_resume_service(db, id, resume)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_resume_service(db, id)