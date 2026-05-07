from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from app.schemas.resume import ResumeCreate,ResumeResponse, ResumeUpdate
from app.db.database import get_db
from app.services.resume_service import add_resume_service,get_resume_services,get_resume_service,delete_resume_service,get_user_resumes,update_resume_service
from app.core.oauth2 import get_current_user, get_admin_user
from typing import List


router = APIRouter(
    prefix='/resumes',
    tags=['Resumes']
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=ResumeResponse)
def add_resume(resume:ResumeCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return add_resume_service(db,resume)



@router.get('/',status_code=status.HTTP_200_OK,response_model=List[ResumeResponse])
def get_resumes(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    role_value = current_user.role.value if hasattr(current_user.role, 'value') else current_user.role
    if role_value == "admin":
        resumes = get_resume_services(db)
    else:
        resumes = get_user_resumes(db, current_user.id)
    return resumes



@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=ResumeResponse)
def get_resume(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    resume = get_resume_service(db,id)
    return resume

@router.put('/{id}',status_code=status.HTTP_200_OK,response_model=ResumeResponse)
def put_resume(id:int,resume:ResumeUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return update_resume_service(db, id, resume)

@router.patch('/{id}',status_code=status.HTTP_200_OK,response_model=ResumeResponse)
def patch_resume(id:int,resume:ResumeUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return update_resume_service(db, id, resume)

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return delete_resume_service(db,id)