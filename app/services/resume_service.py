import os
from sqlalchemy.orm import Session
from app.models.resume import Resume
from fastapi import HTTPException, status
from .pdf_service import extract_text_from_pdf
from app.ai.rag.indexer import embed_resume


def add_resume_service(db: Session, file_name: str, file_path: str, user_id: int):
    extracted_text = extract_text_from_pdf(file_path)

    db_resume = Resume(
        user_id=user_id,
        file_name=file_name,
        file_path=file_path,
        extracted_text=extracted_text,
        is_active=True
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)

    
    try:
        if extracted_text:
            embed_resume(db_resume.id, extracted_text)
    except Exception as e:
        print(f"[WARNING] ChromaDB embedding failed for resume {db_resume.id}: {e}")

    return db_resume


def get_resume_services(db: Session):
    return db.query(Resume).all()


def get_user_resumes(db: Session, user_id: int):
    return db.query(Resume).filter(Resume.user_id == user_id).all()


def get_resume_service(db: Session, resume_id: int):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {resume_id} not found"
        )
    return resume


def update_resume_service(db: Session, resume_id: int, resume_update):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {resume_id} not found"
        )
    update_data = resume_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(resume, key, value)
    db.commit()
    db.refresh(resume)
    return resume


def delete_resume_service(db: Session, resume_id: int):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {resume_id} not found"
        )
    db.delete(resume)
    db.commit()
    return None
