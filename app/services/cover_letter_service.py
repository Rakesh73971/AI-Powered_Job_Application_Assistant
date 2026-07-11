from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from app.models.coverletter import CoverLetterHistory
from app.models.analysis import AnalysisReport
from app.models.resume import Resume
from app.models.jobdescription import JobDescription
from app.ai.rag.retriever import retrieve_resume_context, retrieve_jd_context
from app.ai.chains.cover_letter_chain import cover_chain, generate_cover_letter_chain


def generate_cover_letter_service(db: Session, analysis_id: int, tone: str):
    """
    Generate a cover letter using RAG context + Gemini.
    Saves the result to CoverLetterHistory and returns the record.
    """
    analysis = db.query(AnalysisReport).filter(AnalysisReport.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    resume = db.query(Resume).filter(Resume.id == analysis.resume_id).first()
    jd = db.query(JobDescription).filter(JobDescription.id == analysis.jd_id).first()

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

    db.add(letter)

    # Save latest cover letter in analyses table
    analysis.cover_letter = content

    db.commit()
    db.refresh(letter)

    return letter


async def stream_cover_letter(analysis_id: int, tone: str, db: Session):
    """
    Async generator that streams cover letter tokens via SSE.
    """
    analysis = db.query(AnalysisReport).filter(AnalysisReport.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    resume = db.query(Resume).filter(Resume.id == analysis.resume_id).first()
    jd = db.query(JobDescription).filter(JobDescription.id == analysis.jd_id).first()

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

        db.add(letter)

        analysis.cover_letter = full_content

        db.commit()
    except Exception as e:
        print(f"[WARNING] Failed to save cover letter to DB: {e}")


def create_cover_letter_service(db: Session, cover_letter):

    letter = CoverLetterHistory(
        report_id=cover_letter.report_id,
        tone=cover_letter.tone,
        content=cover_letter.content
    )

    db.add(letter)

    analysis = db.query(AnalysisReport).filter(
        AnalysisReport.id == cover_letter.report_id
    ).first()

    if analysis:
        analysis.cover_letter = cover_letter.content

    db.commit()
    db.refresh(letter)

    return letter


def get_cover_letters_service(db: Session):
    return db.query(CoverLetterHistory).all()


def get_cover_letter_service(db: Session, letter_id: int):
    cover_letter = db.query(CoverLetterHistory).filter(CoverLetterHistory.id == letter_id).first()
    if not cover_letter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cover letter with id {letter_id} not found"
        )
    return cover_letter


def update_cover_letter_service(db: Session, letter_id: int, cover_letter_update):
    cover_letter = db.query(CoverLetterHistory).filter(CoverLetterHistory.id == letter_id).first()
    if not cover_letter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cover letter with id {letter_id} not found"
        )
    update_data = cover_letter_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cover_letter, key, value)
    db.commit()
    db.refresh(cover_letter)
    return cover_letter


def delete_cover_letter(db: Session, letter_id: int):
    cover_letter = db.query(CoverLetterHistory).filter(CoverLetterHistory.id == letter_id).first()
    if not cover_letter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cover letter with id {letter_id} not found"
        )
    db.delete(cover_letter)
    db.commit()
    return None
