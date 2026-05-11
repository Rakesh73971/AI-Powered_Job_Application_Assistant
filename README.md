# AI-Powered Job Application Assistant

An intelligent backend system designed to help job seekers optimize their application process using AI-driven insights, document analysis, and automated content generation.

## 🚀 Overview

The **AI-Powered Job Application Assistant** is a robust FastAPI-based backend that leverages Retrieval-Augmented Generation (RAG) with Google Gemini and LangChain to provide tailored resume analysis, cover letter generation, and job matching capabilities.

### Key Features

- **🔐 Secure Authentication**: JWT-based user authentication and authorization.
- **📄 Resume Management**: Upload and parse PDF resumes using `pdfplumber`.
- **🔍 JD Analysis**: Extract key requirements and skills from job descriptions.
- **🧠 RAG Pipeline**: Intelligent document retrieval using ChromaDB for context-aware AI responses.
- **✍️ Automated Cover Letters**: Generate professional, tailored cover letters with real-time SSE streaming.
- **⚙️ Async Processing**: Offload heavy AI tasks to Celery workers backed by Redis.
- **🛠️ API Documentation**: Interactive Swagger UI and Redoc available out of the box.

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI/LLM**: [Google Gemini Pro](https://ai.google.dev/) via [LangChain](https://www.langchain.com/)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **Primary Database**: [PostgreSQL](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/)
- **Task Queue**: [Celery](https://docs.celeryq.dev/) + [Redis](https://redis.io/)
- **Document Parsing**: `pdfplumber`
- **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.10+
- Docker & Docker Compose (optional but recommended)
- A Google Gemini API Key

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Rakesh73971/AI-Powered_Job_Application_Assistant.git
cd AI-Powered_Job_Application_Assistant
```

### 2. Environment Configuration
Create a `.env` file in the root directory and add your credentials:
```env
# Database Configuration
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_db_password
DATABASE_NAME=ai_job_assistant
DATABASE_USERNAME=postgres

# Auth Configuration
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google API Key
GOOGLE_API_KEY=your_gemini_api_key

# Redis & Celery
REDIS_URL=redis://localhost:6379/0
```

### 3. Local Setup (Without Docker)

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

**Start Redis (Required for Celery):**
Ensure Redis is running locally on port 6379.

**Run the Application:**
```bash
uvicorn app.main:app --reload
```

**Run Celery Worker:**
```bash
celery -A celery_worker.celery_app worker --loglevel=info
```

### 4. Docker Deployment (Recommended)
Simply run:
```bash
docker-compose up --build
```
This will spin up the FastAPI app, Celery worker, PostgreSQL, and Redis.

---

## 📖 API Usage

Once the server is running, access the interactive documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **Redoc**: `http://localhost:8000/redoc`

### Core Endpoints

| Category | Endpoint | Method | Description |
| :--- | :--- | :--- | :--- |
| **Auth** | `/login` | `POST` | Get JWT access token |
| **User** | `/users` | `POST` | Register a new user |
| **Resume** | `/resumes/upload` | `POST` | Upload and parse PDF resume |
| **JD** | `/job-descriptions` | `POST` | Submit a job description |
| **Analysis** | `/analyze` | `POST` | Match resume with JD |
| **Stream** | `/stream/cover-letter` | `GET` | Stream generated cover letter (SSE) |

---

## 🏗️ Project Structure

```text
├── app/
│   ├── core/           # Config and Security
│   ├── db/             # Database connection and models
│   ├── models/         # SQLAlchemy Models
│   ├── routers/        # API Endpoints
│   ├── schemas/        # Pydantic Schemas (Data Validation)
│   ├── services/       # Business Logic (AI, RAG, Parsing)
│   ├── tasks/          # Celery Background Tasks
│   └── main.py         # Application Entry Point
├── celery_worker.py    # Celery App Instance
├── docker-compose.yml  # Docker Orchestration
├── requirements.txt    # Project Dependencies
└── uploads/            # Local storage for resumes
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed with ❤️ by [Rakesh](https://github.com/Rakesh73971)*
