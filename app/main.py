from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Company(BaseModel):
    name: str


@app.get("/")
def root():
    return {"message": "Enterprise Data API"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}


@app.get("/companies/{company_id}")
def get_company(company_id: int):
    return {"company_id": company_id}


@app.post("/companies")
def create_company(company: Company):
    return company