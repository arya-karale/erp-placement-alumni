from fastapi import FastAPI
from app.database import Base, engine
from app.routes import admin_company, student, admin_drive, admin_round

app = FastAPI(title="College ERP – Placement Module")

Base.metadata.create_all(bind=engine)

app.include_router(admin_company.router)
app.include_router(student.router)
app.include_router(admin_drive.router)
app.include_router(admin_round.router)

@app.get("/")
def root():
    return {"message": "ERP Placement Backend is running 🚀"}