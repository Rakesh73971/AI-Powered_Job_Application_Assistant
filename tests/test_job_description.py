def test_description(authorized_access):
    request_data = {
        "company_name":"ResoluteAI Software",
        "role_title":"Python Developer",
        "jd_text":"Fresher Role,Python,Django,FastAPI,MySQL,PostgreSQL,hands on experience and exposure to projects and internships"
    }
    response = authorized_access.post('/job_descriptions/',json=request_data)
    assert response.json()["company_name"] == "ResoluteAI Software"

def test_get_job_descriptions(authorized_access):
    response = authorized_access.get("/job_descriptions/")
    assert response.status_code == 200

def test_get_job_description(authorized_access,test_job_description):
    response = authorized_access.get(f"/job_descriptions/{test_job_description["id"]}")
    assert response.status_code == 200
    assert response.json()["company_name"] == "ResoluteAI Software"

def test_update_job_description(authorized_access,test_job_description):
    request_data = {
        "role_title":"Backend Developer"
    }
    response = authorized_access.patch(f"/job_descriptions/{test_job_description["id"]}",json=request_data)
    assert response.status_code == 200
    assert response.json()["role_title"] == "Backend Developer"

def test_delete_job_descripton(authorized_access,test_job_description):
    response = authorized_access.delete(f"/job_descriptions/{test_job_description["id"]}")
    assert response.status_code == 204