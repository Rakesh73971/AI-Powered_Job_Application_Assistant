from sqlalchemy.ext.asyncio import AsyncSession
from app.models.analysis import AnalysisReport, Status
from fastapi import status, HTTPException
from sqlalchemy import select

async def create_analysis(db: AsyncSession, analysis, current_user):
    """Create analysis record and dispatch Celery task for async processing."""
    db_analysis = AnalysisReport(
        user_id=current_user.id,
        resume_id=analysis.resume_id,
        jd_id=analysis.jd_id,
        status=Status.PENDING
    )
    db.add(db_analysis)
    await db.commit()
    await db.refresh(db_analysis)

    
    try:
        from app.tasks.analysis_task import run_analysis_task
        task = run_analysis_task.delay(db_analysis.id)
        db_analysis.task_id = task.id
        await db.commit()
        await db.refresh(db_analysis)
    except Exception as e:
        print(f"[WARNING] Celery dispatch failed: {e}. Analysis will stay PENDING.")

    return db_analysis


async def get_analyses(db: AsyncSession):
    result = await db.execute(select(AnalysisReport))
    analysis = result.scalars().all()
    return analysis


async def get_analysis(db: AsyncSession, analysis_id: int):
    results = await db.execute(select(AnalysisReport).where(AnalysisReport.id == analysis_id))

    analysis = results.scalar_one_or_none()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis report with id {analysis_id} not found"
        )
    return analysis


async def get_analysis_status(db: AsyncSession, analysis_id: int):
    """Returns DB record + live Celery task status."""
    analysis = get_analysis(db, analysis_id)
    celery_status = None
    error_message = None

    if analysis.task_id:
        try:
            from celery_worker import celery_app
            task_result = celery_app.AsyncResult(analysis.task_id)
            celery_status = task_result.state
            if celery_status == 'FAILURE':
                error_message = str(task_result.result) if task_result.result else "Unknown error"
        except Exception:
            celery_status = "UNKNOWN"

    return {
        "id": analysis.id,
        "task_id": analysis.task_id,
        "db_status": analysis.status.value if hasattr(analysis.status, 'value') else analysis.status,
        "celery_status": celery_status,
        "error_message": error_message,
        "match_score": analysis.match_score,
        "missing_skills": analysis.missing_skills,
        "weak_sections": analysis.weak_sections,
        "suggestions": analysis.suggestions,
        "created_at": analysis.created_at.isoformat()
    }


async def update_analysis(db: AsyncSession, analysis_id: int, analysis_update):
    results = await db.execute(select(AnalysisReport).where(AnalysisReport.id == analysis_id))
    analysis = results.scalar_one_or_none()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis report with id {analysis_id} not found"
        )
    update_data = analysis_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(analysis, key, value)
    await db.commit()
    await db.refresh(analysis)
    return analysis


async def delete_analysis(db: AsyncSession, analysis_id: int):
    results = await db.execute(select(AnalysisReport).where(AnalysisReport.id == analysis_id))
    analysis = results.scalar_one_or_none()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis report with id {analysis_id} not found"
        )
    await db.delete(analysis)
    await db.commit()
    return None
