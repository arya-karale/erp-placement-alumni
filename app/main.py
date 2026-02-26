from fastapi import FastAPI
from app.database import Base, engine
from app.routes import admin_company, admin_drive
from app.routes import admin_company, student

app = FastAPI(title="College ERP – Placement Module")

Base.metadata.create_all(bind=engine)

app.include_router(admin_company.router)
app.include_router(student.router)

@app.get("/")
def root():
    return {"message": "ERP Placement Backend is running"}
