from fastapi import APIRouter

from app.db.connection import get_connection
from app.schemas import CompanyCreate, CompanyResponse

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/{company_id}")
def get_company(company_id: int):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, industry FROM companies WHERE id = %s",
                (company_id,),
            )
            company = cursor.fetchone()

        return {
            "id": company[0],
            "name": company[1],
            "industry": company[2]
        }


@router.post("", response_model=CompanyResponse)
def create_company(company: CompanyCreate):
    return {
        "id":1,
        "name": company.name,
        "industry": company.industry,
    }