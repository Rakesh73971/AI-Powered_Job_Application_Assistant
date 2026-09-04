from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.resume import Resume
from .pdf_service import extract_text_from_pdf
from app.ai.rag.indexer import embed_resume


async def add_resume_service(
    db: AsyncSession,
    file_name: str,
    file_path: str,
    user_id: int
):
    extracted_text = extract_text_from_pdf(file_path)

    db_resume = Resume(
        user_id=user_id,
        file_name=file_name,
        file_path=file_path,
        extracted_text=extracted_text,
        is_active=True
    )

    db.add(db_resume)

    await db.commit()
    await db.refresh(db_resume)

    try:
        if extracted_text:
            embed_resume(
                db_resume.id,
                extracted_text
            )
    except Exception as e:
        print(
            f"[WARNING] ChromaDB embedding failed "
            f"for resume {db_resume.id}: {e}"
        )

    return db_resume


async def get_resume_services(
    db: AsyncSession
):
    result = await db.execute(
        select(Resume)
    )

    return result.scalars().all()


async def get_user_resumes(
    db: AsyncSession,
    user_id: int
):
    result = await db.execute(
        select(Resume).where(
            Resume.user_id == user_id
        )
    )

    return result.scalars().all()


async def get_resume_service(
    db: AsyncSession,
    resume_id: int
):
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id
        )
    )

    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {resume_id} not found"
        )

    return resume


async def update_resume_service(
    db: AsyncSession,
    resume_id: int,
    resume_update
):
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id
        )
    )

    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {resume_id} not found"
        )

    update_data = resume_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(resume, key, value)

    await db.commit()
    await db.refresh(resume)

    return resume


async def delete_resume_service(
    db: AsyncSession,
    resume_id: int
):
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id
        )
    )

    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {resume_id} not found"
        )

    await db.delete(resume)
    await db.commit()

    return None