from celery_worker import celery_app
from app.db.database import SessionLocal
from app.models.analysis import AnalysisReport, Status
from app.models.resume import Resume
from app.models.jobdescription import JobDescription
from app.services.rag_service import retrieve_resume_context, retrieve_jd_context
from app.services.llm_service import gap_chain


@celery_app.task(bind=True, name="run_analysis_task")
def run_analysis_task(self, analysis_id: int):
    """
    Background task that:
    1. Fetches the AnalysisReport, Resume, and JD from DB
    2. Retrieves relevant chunks from ChromaDB via RAG
    3. Invokes the Gemini gap analysis chain
    4. Stores structured results back to DB
    """
    db = SessionLocal()
    try:
        
        report = db.query(AnalysisReport).filter(AnalysisReport.id == analysis_id).first()
        if not report:
            return {"error": f"AnalysisReport {analysis_id} not found"}

        report.status = Status.PROCESSING
        db.commit()

        
        resume = db.query(Resume).filter(Resume.id == report.resume_id).first()
        jd = db.query(JobDescription).filter(JobDescription.id == report.jd_id).first()

        if not resume or not jd:
            report.status = Status.FAILED
            db.commit()
            return {"error": "Resume or JD not found"}

        
        query = f"{jd.role_title} at {jd.company_name}"
        resume_context = retrieve_resume_context(report.resume_id, query) or (resume.extracted_text or "")
        jd_context = retrieve_jd_context(report.jd_id, query) or jd.jd_text

        
        result = gap_chain.invoke({
            "resume_context": resume_context,
            "jd_context": jd_context
        })

        
        report.match_score = float(result.get("match_score", 0))
        report.missing_skills = result.get("missing_skills", [])
        report.weak_sections = result.get("weak_sections", [])
        report.suggestions = result.get("suggestions", [])
        report.status = Status.COMPLETED
        db.commit()

        return {
            "analysis_id": analysis_id,
            "match_score": report.match_score,
            "status": "completed"
        }

    except Exception as exc:
        db.rollback()
        
        try:
            report = db.query(AnalysisReport).filter(AnalysisReport.id == analysis_id).first()
            if report:
                report.status = Status.FAILED
                db.commit()
        except Exception:
            pass
        raise self.retry(exc=exc, max_retries=2, countdown=5)

    finally:
        db.close()
