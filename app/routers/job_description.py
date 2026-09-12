from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.jobdescription import JobDescriptionResponse,JodDescriptionCreate, JobDescriptionUpdate
from app.db.database import get_db
from app.core.oauth2 import get_current_user, get_admin_user
from app.services.job_desc_service import create_job_desc,get_job_descs,get_job_desc,delete_job_desc, update_job_desc
from typing import List

router = APIRouter(
    prefix='/job_descriptions',
    tags=['JobDescriptions']
)


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=JobDescriptionResponse)
async def create_job_description(job_desc:JodDescriptionCreate,db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    job_desc = create_job_desc(db, job_desc,current_user)
    return await job_desc



@router.get('/',status_code=status.HTTP_200_OK,response_model=List[JobDescriptionResponse])
async def get_job_descriptions(db:AsyncSession=Depends(get_db),current_user=Depends(get_admin_user)):
    job_descriptions = get_job_descs(db)
    return await job_descriptions



@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=JobDescriptionResponse)
async def get_job_description(id:int,db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    job_description = get_job_desc(db,id)
    return await job_description

@router.put('/{id}',status_code=status.HTTP_200_OK,response_model=JobDescriptionResponse)
async def put_job_description(id:int,job_desc:JobDescriptionUpdate,db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    return await update_job_desc(db, id, job_desc)

@router.patch('/{id}',status_code=status.HTTP_200_OK,response_model=JobDescriptionResponse)
async def patch_job_description(id:int,job_desc:JobDescriptionUpdate,db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    return await update_job_desc(db, id, job_desc)


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_description(id:int,db:AsyncSession=Depends(get_db),current_user=Depends(get_current_user)):
    return await delete_job_desc(db,id)