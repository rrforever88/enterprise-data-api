from fastapi.testclient import TestClient

from app.main import app

from app.db.connection import get_connection

client = TestClient(app)

def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Enterprise Data API"}

def test_get_company():
    response = client.get("/companies/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Company not found"}

def test_get_company_id():
    response = client.get("/companies/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Acme",
        "industry": "Manufacturing"
    }

def test_post_company():
    response = client.post(
        "/companies",
        json={
            "name": "Globex",
            "industry": "Technology"
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Globex"
    assert data["industry"] == "Technology"
    assert isinstance(data['id'], int)

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT name, industry
                FROM companies
                WHERE name = %s
                """,
                ("Globex",),
            )
            company = cursor.fetchone()

    assert company == ("Globex", "Technology")

def test_post_company_dup():
    response = client.post(
        "/companies",
        json={
            "name": "Acme",
            "industry": "Manufacturing"
        },
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Company already exists"}

def test_create_contact():
    response = client.post(
        "/contacts",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "company_id": 1
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["company_id"] == 1
    assert isinstance(data['id'], int)

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT name, email, company_id
                FROM contacts
                WHERE name = %s
                """,
                ("John Doe",),
            )
            contact = cursor.fetchone()

    assert contact == ("John Doe", "john@example.com", 1)

def test_post_contact_invalid_foreign_key():
    response = client.post(
        "/contacts",
        json={
            "name": "Bad Company",
            "email": "bad@example.com",
            "company_id": 999,
        },
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Invalid company_id"}