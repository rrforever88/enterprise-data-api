from fastapi import APIRouter, HTTPException
from psycopg.errors import UniqueViolation

from app.db.connection import get_connection
from app.schemas import CompanyCreate, CompanyResponse, ContactResponse

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, industry FROM companies WHERE id = %s",
                (company_id,),
            )
            company = cursor.fetchone()

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return {
        "id": company[0],
        "name": company[1],
        "industry": company[2]
    }

@router.get(
        "/{company_id}/contacts",
        response_model=list[ContactResponse],
)
def get_contacts_by_company(company_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, company_id, name, email
                FROM contacts
                WHERE company_id = %s
                """,
                (company_id,),
            )
            contacts = cursor.fetchall()

    return [
    {
        "id": contact[0],
        "company_id": contact[1],
        "name": contact[2],
        "email": contact[3]
    }
    for contact in contacts
]


@router.post("", response_model=CompanyResponse, status_code=201)
def create_company(company: CompanyCreate):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO companies (name, industry)
                    VALUES (%s, %s)
                    RETURNING id, name, industry
                    """,
                    (company.name, company.industry),
                )
                new_company = cursor.fetchone()

    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Company already exists",
        )

    return {
        "id": new_company[0],
        "name": new_company[1],
        "industry": new_company[2]
    }