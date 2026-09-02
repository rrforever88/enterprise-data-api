from fastapi import APIRouter


from app.schemas import CompanyCreate, CompanyResponse

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("/{company_id}")
def get_company(company_id: int):
    return {"company_id": company_id}


@router.post("", response_model=CompanyResponse)
def create_company(company: CompanyCreate):
    return {
        "id":1,
        "name": company.name,
        "industry": company.industry,
    }