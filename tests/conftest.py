from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.db.database import Base, get_db
from app.core.oauth2 import create_access_token
import pytest
import asyncio

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture
def session():
    async def reset_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    
    asyncio.run(reset_db())
    yield

@pytest.fixture
def client(session):
    async def override_get_db():
        async with TestingSessionLocal() as db_session:
            yield db_session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(client):
    user_data={
        'full_name':'Rakesh',
        'email':'rakesh@gmail.com',
        'password':'password123',
        'role':'admin'
    }

    response = client.post('/users/',json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id':test_user['id']})


@pytest.fixture
def authorized_access(client,token):
    client.headers = {
        **client.headers,
        'Authorization':f'Bearer {token}'
    }
    return client


@pytest.fixture
def test_resume(authorized_access):
    response = authorized_access.post(
        "/resumes/",
        files={
            "file": ("Rakesh.pdf", b"dummy pdf content", "application/pdf")
        }
    )
    return response.json()

@pytest.fixture
def test_job_description(authorized_access):
    request_data = {
        "company_name":"ResoluteAI Software",
        "role_title":"Python Developer",
        "jd_text":"Fresher Role,Python,Django,FastAPI,MySQL,PostgreSQL,hands on experience and exposure to projects and internships"
    }
    response = authorized_access.post('/job_descriptions/',json=request_data)
    return response.json()

@pytest.fixture
def test_analysis_report(authorized_access, test_resume, test_job_description):
    payload = {
        "resume_id": test_resume["id"],
        "jd_id": test_job_description["id"]
    }
    response = authorized_access.post("/analyses/", json=payload)
    return response.json()

@pytest.fixture
def test_cover_letter(authorized_access,test_analysis_report):
    payload = {
        "report_id":test_analysis_report['id'],
        "tone":"formal",
        "content":"Dear Manager, I am computer science student and I am willing to work with you. My skills are alligned with the requirements"
    }
    response = authorized_access.post('/cover_letters/',json=payload)
    return response.json()