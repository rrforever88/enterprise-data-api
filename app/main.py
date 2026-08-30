from fastapi import FastAPI

from app.routes import companies, contacts

app = FastAPI()


app.include_router(companies.router)
app.include_router(contacts.router)

@app.get("/")
def root():
    return {"message": "Enterprise Data API"}

