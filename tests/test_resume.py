
def test_create_resumes(authorized_access):
    response = authorized_access.post(
        "/resumes/",
        files={
            "file": ("Rakesh.pdf", b"dummy pdf content", "application/pdf")
        }
    )

    assert response.status_code == 201

def test_get_resumes(authorized_access):
    response = authorized_access.get('/resumes/')
    assert response.status_code == 200

def test_get_resume(authorized_access,test_resume):
    resume_id = test_resume["id"]
    response = authorized_access.get(f"/resumes/{resume_id}")
    assert response.status_code == 200

def test_update_resume(authorized_access,test_resume):
    request_data = {
        "file_name":"Prakash.pdf"
    }
    resume_id = test_resume["id"]
    response = authorized_access.patch(f"/resumes/{resume_id}",json=request_data)
    assert response.status_code == 200
    assert response.json()['file_name'] == "Prakash.pdf"



def test_delete_resume(authorized_access,test_resume):
    resume_id = test_resume['id']
    response = authorized_access.delete(f"/resumes/{resume_id}")
    assert response.status_code == 204