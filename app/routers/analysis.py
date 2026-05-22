from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.analysis import AnalysisReportResponse, AnalysisReportCreate, AnalysisReportUpdate
from app.db.database import get_db
from app.core.oauth2 import get_current_user, get_admin_user
from app.services.analysis_service import (
    create_analysis, get_analyses, get_analysis,
    update_analysis, delete_analysis, get_analysis_status
)
from typing import List, Any

router = APIRouter(
    prefix='/analyses',
    tags=['Analyses']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AnalysisReportResponse)
def create_analysis_report(
    analysis: AnalysisReportCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    return create_analysis(db, analysis, current_user)


@router.get('/status/{id}', status_code=status.HTTP_200_OK)
def poll_analysis_status(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
) -> Any:
    
    return get_analysis_status(db, id)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[AnalysisReportResponse])
def get_all_analyses(db: Session = Depends(get_db), current_user=Depends(get_admin_user)):
    return get_analyses(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=AnalysisReportResponse)
def get_analysis_report(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_analysis(db, id)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=AnalysisReportResponse)
def put_analysis_report(id: int, analysis: AnalysisReportUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_analysis(db, id, analysis)


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=AnalysisReportResponse)
def patch_analysis_report(id: int, analysis: AnalysisReportUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return update_analysis(db, id, analysis)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis_report(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return delete_analysis(db, id)
