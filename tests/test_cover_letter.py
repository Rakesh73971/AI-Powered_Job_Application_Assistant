def test_create_cover_letter(authorized_access,test_analysis_report):
    payload = {
        "report_id":test_analysis_report['id'],
        "tone":"formal",
        "content":"Dear Manager, I am computer science student and I am willing to work with you. My skills are alligned with the requirements"
    }
    response = authorized_access.post('/cover_letters/',json=payload)
    assert response.status_code == 201
    assert response.json()["tone"] == "formal"

def test_get_cover_letters(authorized_access):
    response = authorized_access.get("/cover_letters/")
    assert response.status_code == 200

def test_get_cover_letter(authorized_access,test_cover_letter):
    response = authorized_access.get(f"/cover_letters/{test_cover_letter["id"]}")
    assert response.status_code == 200
    assert response.json()["tone"] == "formal"


def test_update_cover_letter(authorized_access,test_cover_letter):
    payload = {
        "tone":"stylish"
    }
    response = authorized_access.patch(f"/cover_letters/{test_cover_letter['id']}",json=payload)
    assert response.status_code == 200
    assert response.json()["tone"] == "stylish"


def test_delete_cover_letter(authorized_access,test_cover_letter):
    response = authorized_access.delete(f"/cover_letters/{test_cover_letter['id']}")
    assert response.status_code == 204
