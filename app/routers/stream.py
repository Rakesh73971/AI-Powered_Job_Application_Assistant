from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse
from app.db.database import get_db
from app.core.oauth2 import get_current_user
from app.services.cover_letter_service import stream_cover_letter, generate_cover_letter_service
from app.schemas.cover_letter import CoverLetterResponse

router = APIRouter(
    prefix='/stream',
    tags=['Streaming']
)


@router.get('/cover_letter', response_class=EventSourceResponse)
async def stream_cover_letter_endpoint(
    analysis_id: int = Query(..., description="ID of the AnalysisReport to generate cover letter for"),
    tone: str = Query("professional", description="Tone of cover letter: professional, conversational, enthusiastic"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Stream a cover letter token-by-token via Server-Sent Events (SSE).
    The completed letter is automatically saved to CoverLetterHistory in DB.

    Usage: GET /stream/cover_letter?analysis_id=1&tone=professional
    """
    async def event_generator():
        try:
            async for token in stream_cover_letter(analysis_id, tone, db):
                yield {"data": token}
            yield {"data": "[DONE]"}
        except Exception as e:
            yield {"data": f"[ERROR] {str(e)}"}

    return EventSourceResponse(event_generator())


@router.post('/cover_letter/generate', response_model=CoverLetterResponse)
def generate_cover_letter_endpoint(
    analysis_id: int = Query(...),
    tone: str = Query("professional"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Non-streaming version: generate and save a cover letter synchronously.
    Returns the full CoverLetterHistory record.
    """
    return generate_cover_letter_service(db, analysis_id, tone)
