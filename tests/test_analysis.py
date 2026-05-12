def test_create_analysis_report(authorized_access, test_resume, test_job_description):
    payload = {
        "resume_id": test_resume["id"],
        "jd_id": test_job_description["id"]
    }
    response = authorized_access.post("/analyses/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["resume_id"] == test_resume["id"]
    assert data["jd_id"] == test_job_description["id"]
    assert data["status"] == "pending"
    assert "id" in data
    assert "task_id" in data or data["task_id"] is None

def test_get_analysis_reports(authorized_access):
    response = authorized_access.get("/analyses/")
    assert response.status_code == 200

def test_get_analysis_report(authorized_access,test_analysis_report):
    response = authorized_access.get(f"/analyses/{test_analysis_report['id']}")
    assert response.status_code == 200

def test_update_analysis_report(authorized_access,test_analysis_report):
    update_payload = {"match_score":85.5,"status":"completed"}
    response = authorized_access.put(f"/analyses/{test_analysis_report['id']}",json=update_payload)
    assert response.status_code == 200
    assert response.json()["match_score"] == 85.5
    assert response.json()["status"] == "completed"



def test_delete_analysis_report(authorized_access,test_analysis_report):
    response = authorized_access.delete(f"/analyses/{test_analysis_report['id']}")
    assert response.status_code == 204