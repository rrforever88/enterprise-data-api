from fastapi import APIRouter

from app.schemas import ContactCreate, ContactResponse

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("", response_model=ContactResponse)
def create_contact(contact: ContactCreate):
    return {
        "id":1,
        "name": contact.name,
        "email": contact.email,
        "company_id": contact.company_id,
    }