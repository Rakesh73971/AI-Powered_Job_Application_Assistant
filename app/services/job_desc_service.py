from sqlalchemy.orm import Session
from app.models.jobdescription import JobDescription
from fastapi import status, HTTPException
from app.services.embedding_service import embed_jd


def create_job_desc(db: Session, job, current_user):
    db_job = JobDescription(
        user_id=current_user.id,
        company_name=job.company_name,
        role_title=job.role_title,
        jd_text=job.jd_text,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    # Index JD chunks in ChromaDB for RAG
    try:
        if db_job.jd_text:
            embed_jd(db_job.id, db_job.jd_text)
    except Exception as e:
        print(f"[WARNING] ChromaDB embedding failed for JD {db_job.id}: {e}")

    return db_job


def get_job_descs(db: Session):
    return db.query(JobDescription).all()


def get_job_desc(db: Session, jd_id: int):
    job_desc = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not job_desc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job description with id {jd_id} not found"
        )
    return job_desc


def update_job_desc(db: Session, jd_id: int, job_update):
    job_desc = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not job_desc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job description with id {jd_id} not found"
        )
    update_data = job_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job_desc, key, value)
    db.commit()
    db.refresh(job_desc)
    return job_desc


def delete_job_desc(db: Session, jd_id: int):
    job_desc = db.query(JobDescription).filter(JobDescription.id == jd_id).first()
    if not job_desc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job description with id {jd_id} not found"
        )
    db.delete(job_desc)
    db.commit()
    return None