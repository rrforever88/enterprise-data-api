from fastapi import APIRouter

from app.schemas import CompanyCreate

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/{company_id}")
def get_company(company_id: int):
    return {"company_id": company_id}


@router.post("")
def create_company(company: CompanyCreate):
    return company