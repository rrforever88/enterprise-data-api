from fastapi import FastAPI

from app.schemas import CompanyCreate, ContactCreate

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Enterprise Data API"}



@app.get("/companies/{company_id}")
def get_company(company_id: int):
    return {"company_id": company_id}


@app.post("/companies")
def create_company(company: CompanyCreate):
    return company


@app.post("/contacts")
def create_contact(contact: ContactCreate):
    return contact