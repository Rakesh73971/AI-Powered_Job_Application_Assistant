from fastapi import status,HTTPException
from sqlalchemy.orm import Session
from app.models.coverletter import CoverLetterHistory

def create_cover_letter_service(db:Session,cover_letter):
    cover_letter = CoverLetterHistory(
        report_id = cover_letter.report_id,
        tone = cover_letter.tone,
        content = cover_letter.content
    )
    db.add(cover_letter)
    db.commit()
    db.refresh(cover_letter)
    return cover_letter

def get_cover_letters_service(db:Session):
    cover_letters = db.query(CoverLetterHistory).all()
    return cover_letters

def get_cover_letter_service(db:Session,letter_id):
    cover_letter = db.query(CoverLetterHistory).filter(CoverLetterHistory.id == letter_id).first()
    if not cover_letter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'cover letter with id {letter_id} not found')
    return cover_letter

def update_cover_letter_service(db:Session,letter_id,cover_letter_update):
    cover_letter = db.query(CoverLetterHistory).filter(CoverLetterHistory.id == letter_id).first()
    if not cover_letter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'cover letter with id {letter_id} not found')
    
    update_data = cover_letter_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cover_letter, key, value)
        
    db.commit()
    db.refresh(cover_letter)
    return cover_letter

def delete_cover_letter(db:Session,letter_id):
    cover_letter = db.query(CoverLetterHistory).filter(CoverLetterHistory.id == letter_id).first()
    if not cover_letter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'cover letter with id {letter_id} not found')
    db.delete(cover_letter)
    db.commit()
    return None