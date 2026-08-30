from fastapi import APIRouter

from app.schemas import ContactCreate

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("")
def create_contact(contact: ContactCreate):
    return contact