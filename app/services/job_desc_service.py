from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import status, HTTPException

from app.models.jobdescription import JobDescription
from app.ai.rag.indexer import embed_jd


async def create_job_desc(
    db: AsyncSession,
    job,
    current_user
):
    db_job = JobDescription(
        user_id=current_user.id,
        company_name=job.company_name,
        role_title=job.role_title,
        jd_text=job.jd_text,
    )

    db.add(db_job)

    await db.commit()
    await db.refresh(db_job)

    try:
        if db_job.jd_text:
            embed_jd(
                db_job.id,
                db_job.jd_text
            )
    except Exception as e:
        print(
            f"[WARNING] ChromaDB embedding failed "
            f"for JD {db_job.id}: {e}"
        )

    return db_job


async def get_job_descs(
    db: AsyncSession
):
    result = await db.execute(
        select(JobDescription)
    )

    jobs = result.scalars().all()

    return jobs


async def get_job_desc(
    db: AsyncSession,
    jd_id: int
):
    result = await db.execute(
        select(JobDescription).where(
            JobDescription.id == jd_id
        )
    )

    job_desc = result.scalar_one_or_none()

    if not job_desc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job description with id {jd_id} not found"
        )

    return job_desc


async def update_job_desc(
    db: AsyncSession,
    jd_id: int,
    job_update
):
    result = await db.execute(
        select(JobDescription).where(
            JobDescription.id == jd_id
        )
    )

    job_desc = result.scalar_one_or_none()

    if not job_desc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job description with id {jd_id} not found"
        )

    update_data = job_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(job_desc, key, value)

    await db.commit()
    await db.refresh(job_desc)

    return job_desc


async def delete_job_desc(
    db: AsyncSession,
    jd_id: int
):
    result = await db.execute(
        select(JobDescription).where(
            JobDescription.id == jd_id
        )
    )

    job_desc = result.scalar_one_or_none()

    if not job_desc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job description with id {jd_id} not found"
        )

    await db.delete(job_desc)
    await db.commit()

    return None