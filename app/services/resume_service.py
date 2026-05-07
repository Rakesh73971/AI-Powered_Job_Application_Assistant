from sqlalchemy.orm import Session
from app.models.resume import Resume
from fastapi import HTTPException,status

def add_resume_service(db:Session,resume):
    db_resume = Resume(
        user_id = resume.user_id,
        file_name = resume.file_name,
        file_path = resume.file_path,
        extracted_text = resume.extracted_text,
        is_active = resume.is_active
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def get_resume_services(db:Session):
    resumes = db.query(Resume).all()
    return resumes

def get_user_resumes(db:Session, user_id: int):
    resumes = db.query(Resume).filter(Resume.user_id == user_id).all()
    return resumes

def get_resume_service(db:Session,resume_id):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'resume with id {resume_id} not found')
    return resume

def update_resume_service(db:Session, resume_id: int, resume_update):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'resume with id {resume_id} not found')
    
    update_data = resume_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(resume, key, value)
        
    db.commit()
    db.refresh(resume)
    return resume

def delete_resume_service(db:Session,resume_id):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'resume with id {resume_id} not found')
    db.delete(resume)
    db.commit()
    return None