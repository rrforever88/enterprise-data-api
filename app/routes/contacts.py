from fastapi import APIRouter, HTTPException
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app.db.connection import get_connection
from app.schemas import ContactCreate, ContactResponse

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO contacts (name, email, company_id)
                    VALUES (%s, %s, %s)
                    RETURNING id, company_id, name, email
                    """,
                    (contact.name, contact.email, contact.company_id),
                )
                new_contact = cursor.fetchone()

    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Contact email already exists"
        )

    except ForeignKeyViolation:
        raise HTTPException(
            status_code=409,
            detail="Invalid company_id"
        )

    return {
        "id": new_contact[0],
        "company_id": new_contact[1],
        "name": new_contact[2],
        "email": new_contact[3],
    }