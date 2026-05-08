from sqlalchemy.orm import Session
from app.models.jobdescription import JobDescription
from fastapi import status,HTTPException,Depends
from app.core.oauth2 import get_current_user

def create_job_desc(db:Session,job,current_user=Depends(get_current_user)):
    db_job = JobDescription(
        user_id = current_user.id,
        company_name = job.company_name,
        role_title = job.role_title,
        jd_text = job.jd_text,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job_descs(db:Session):
    job_descriptions = db.query(JobDescription).all()
    return job_descriptions

def get_job_desc(db:Session,jd_id):
    job_desc = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not job_desc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'job description with id {jd_id} not found')
    return job_desc

def update_job_desc(db:Session,jd_id,job_update):
    job_desc = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not job_desc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'job description with id {jd_id} not found')
    
    update_data = job_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job_desc, key, value)
        
    db.commit()
    db.refresh(job_desc)
    return job_desc

def delete_job_desc(db:Session,jd_id):
    job_desc = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not job_desc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'job description with id {jd_id} not found')
    db.delete(job_desc)
    db.commit()
    return job_desc