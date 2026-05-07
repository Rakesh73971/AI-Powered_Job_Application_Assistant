from sqlalchemy.orm import Session
from app.models.analysis import AnalysisReport
from fastapi import status, HTTPException

def create_analysis(db: Session, analysis, user_id: int):
    db_analysis = AnalysisReport(
        user_id=user_id,
        resume_id=analysis.resume_id,
        jd_id=analysis.jd_id
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

def get_analyses(db: Session):
    return db.query(AnalysisReport).all()

def get_analysis(db: Session, analysis_id: int):
    analysis = db.query(AnalysisReport).filter(AnalysisReport.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'analysis report with id {analysis_id} not found')
    return analysis

def update_analysis(db: Session, analysis_id: int, analysis_update):
    analysis = db.query(AnalysisReport).filter(AnalysisReport.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'analysis report with id {analysis_id} not found')
    
    update_data = analysis_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(analysis, key, value)
        
    db.commit()
    db.refresh(analysis)
    return analysis

def delete_analysis(db: Session, analysis_id: int):
    analysis = db.query(AnalysisReport).filter(AnalysisReport.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'analysis report with id {analysis_id} not found')
    
    db.delete(analysis)
    db.commit()
    return analysis
