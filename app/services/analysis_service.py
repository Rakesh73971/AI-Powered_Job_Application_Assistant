from sqlalchemy.orm import Session
from app.models.analysis import AnalysisReport, Status
from fastapi import status, HTTPException


def create_analysis(db: Session, analysis, current_user):
    """Create analysis record and dispatch Celery task for async processing."""
    db_analysis = AnalysisReport(
        user_id=current_user.id,
        resume_id=analysis.resume_id,
        jd_id=analysis.jd_id,
        status=Status.PENDING
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    # Dispatch background task (import here to avoid circular imports)
    try:
        from app.tasks.analysis_task import run_analysis_task
        task = run_analysis_task.delay(db_analysis.id)
        db_analysis.task_id = task.id
        db.commit()
        db.refresh(db_analysis)
    except Exception as e:
        print(f"[WARNING] Celery dispatch failed: {e}. Analysis will stay PENDING.")

    return db_analysis


def get_analyses(db: Session):
    return db.query(AnalysisReport).all()


def get_analysis(db: Session, analysis_id: int):
    analysis = db.query(AnalysisReport).filter(AnalysisReport.id == analysis_id).first()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis report with id {analysis_id} not found"
        )
    return analysis


def get_analysis_status(db: Session, analysis_id: int):
    """Returns DB record + live Celery task status."""
    analysis = get_analysis(db, analysis_id)
    celery_status = None

    if analysis.task_id:
        try:
            from celery_worker import celery_app
            task_result = celery_app.AsyncResult(analysis.task_id)
            celery_status = task_result.state
        except Exception:
            celery_status = "UNKNOWN"

    return {
        "id": analysis.id,
        "task_id": analysis.task_id,
        "db_status": analysis.status.value if hasattr(analysis.status, 'value') else analysis.status,
        "celery_status": celery_status,
        "match_score": analysis.match_score,
        "missing_skills": analysis.missing_skills,
        "weak_sections": analysis.weak_sections,
        "suggestions": analysis.suggestions,
        "created_at": analysis.created_at.isoformat()
    }


def update_analysis(db: Session, analysis_id: int, analysis_update):
    analysis = db.query(AnalysisReport).filter(AnalysisReport.id == analysis_id).first()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis report with id {analysis_id} not found"
        )
    update_data = analysis_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(analysis, key, value)
    db.commit()
    db.refresh(analysis)
    return analysis


def delete_analysis(db: Session, analysis_id: int):
    analysis = db.query(AnalysisReport).filter(AnalysisReport.id == analysis_id).first()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis report with id {analysis_id} not found"
        )
    db.delete(analysis)
    db.commit()
    return None
