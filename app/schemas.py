from pydantic import BaseModel, Field, EmailStr


class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    industry: str = Field(min_length=1, max_length=100)



class CompanyResponse(BaseModel):
    id: int
    name: str
    industry: str



class ContactCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    company_id: int


class ContactResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    company_id: int