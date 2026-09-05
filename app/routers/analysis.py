from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
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
async def create_analysis_report(
    analysis: AnalysisReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    
    return await create_analysis(db, analysis, current_user)


@router.get('/status/{id}', status_code=status.HTTP_200_OK)
async def poll_analysis_status(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
) -> Any:
    
    return await get_analysis_status(db, id)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[AnalysisReportResponse])
async def get_all_analyses(db: AsyncSession = Depends(get_db), current_user=Depends(get_admin_user)):
    return await get_analyses(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=AnalysisReportResponse)
async def get_analysis_report(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await get_analysis(db, id)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=AnalysisReportResponse)
async def put_analysis_report(id: int, analysis: AnalysisReportUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await update_analysis(db, id, analysis)


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=AnalysisReportResponse)
async def patch_analysis_report(id: int, analysis: AnalysisReportUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await update_analysis(db, id, analysis)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis_report(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await delete_analysis(db, id)
