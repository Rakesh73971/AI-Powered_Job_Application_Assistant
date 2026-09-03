from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from app.models.coverletter import CoverLetterHistory
from app.models.analysis import AnalysisReport
from app.models.resume import Resume
from app.models.jobdescription import JobDescription
from app.ai.rag.retriever import retrieve_resume_context, retrieve_jd_context
from app.ai.chains.cover_letter_chain import cover_chain, generate_cover_letter_chain
from sqlalchemy import select


async def generate_cover_letter_service(db: Session, analysis_id: int, tone: str):
    """
    Generate a cover letter using RAG context + Gemini.
    Saves the result to CoverLetterHistory and returns the record.
    """
    result = await db.execute(select(AnalysisReport).where(AnalysisReport.id == analysis_id))
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    result = await db.execute(select(Resume).where(Resume.id == analysis.resume_id))

    resume = result.scalar_one_or_none()

    result1 = await db.execute(select(JobDescription).where(JobDescription.id == analysis.jd_id))
    jd = result1.scalar_one_or_none()

    query = f"{jd.role_title} at {jd.company_name}"
    resume_context = retrieve_resume_context(analysis.resume_id, query) or (resume.extracted_text or "")
    jd_context = retrieve_jd_context(analysis.jd_id, query) or jd.jd_text

    
    raw = generate_cover_letter_chain.invoke({
        "resume_context": resume_context,
        "jd_context": jd_context,
        "tone": tone
    })
    content = raw if isinstance(raw, str) else getattr(raw, "content", str(raw))

    letter = CoverLetterHistory(
        report_id=analysis_id,
        tone=tone,
        content=content
    )

    await db.add(letter)

    # Save latest cover letter in analyses table
    analysis.cover_letter = content

    await db.commit()
    await db.refresh(letter)

    return letter


async def stream_cover_letter(analysis_id: int, tone: str, db: Session):
    """
    Async generator that streams cover letter tokens via SSE.
    """
    result = await db.execute(select(AnalysisReport).where(AnalysisReport.id == analysis_id))
    analysis = result.scalar_one_or_none()

    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    result = await db.execute(select(Resume).where(Resume.id == analysis.resume_id))
    resume = result.scalar_one_or_none()

    result1 = await db.execute(select(JobDescription).where(JobDescription.id == analysis.jd_id))
    jd = result1.scalar_one_or_none()

    query = f"{jd.role_title} at {jd.company_name}"
    resume_context = retrieve_resume_context(analysis.resume_id, query) or (resume.extracted_text or "")
    jd_context = retrieve_jd_context(analysis.jd_id, query) or jd.jd_text

    full_content = ""
    async for chunk in cover_chain.astream({
        "resume_context": resume_context,
        "jd_context": jd_context,
        "tone": tone
    }):
        full_content += chunk
        yield chunk

    
    try:
        letter = CoverLetterHistory(
            report_id=analysis_id,
            tone=tone,
            content=full_content
        )

        await db.add(letter)

        analysis.cover_letter = full_content

        await db.commit()
    except Exception as e:
        print(f"[WARNING] Failed to save cover letter to DB: {e}")


async def create_cover_letter_service(db: Session, cover_letter):

    letter = CoverLetterHistory(
        report_id=cover_letter.report_id,
        tone=cover_letter.tone,
        content=cover_letter.content
    )

    await db.add(letter)

    result = await db.execute(select(AnalysisReport).where(
        AnalysisReport.id == cover_letter.report_id
    ))
    analysis = result.scalar_one_or_none()

    if analysis:
        analysis.cover_letter = cover_letter.content

    await db.commit()
    await db.refresh(letter)

    return letter


async def get_cover_letters_service(db: Session):
    result = await db.execute(select(CoverLetterHistory))
    coverletters = result.scalars().all()
    return coverletters


async def get_cover_letter_service(db: Session, letter_id: int):
    result = await db.execute(select(CoverLetterHistory).where(CoverLetterHistory.id == letter_id))
    cover_letter = result.scalar_one_or_none()
    if not cover_letter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cover letter with id {letter_id} not found"
        )
    return cover_letter


async def update_cover_letter_service(db: Session, letter_id: int, cover_letter_update):
    result = await db.execute(select(CoverLetterHistory).where(CoverLetterHistory.id == letter_id))
    cover_letter = result.scalar_one_or_none()

    if not cover_letter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cover letter with id {letter_id} not found"
        )
    update_data = cover_letter_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cover_letter, key, value)
    await db.commit()
    await db.refresh(cover_letter)
    return cover_letter


async def delete_cover_letter(db: Session, letter_id: int):
    result = await db.execute(select(CoverLetterHistory).where(CoverLetterHistory.id == letter_id))
    cover_letter = result.scalar_one_or_none()
    if not cover_letter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cover letter with id {letter_id} not found"
        )
    await db.delete(cover_letter)
    await db.commit()
    return None
