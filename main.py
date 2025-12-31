from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import shutil

from database import SessionLocal, engine
from models import Base
from schemas import EmployeeCreate, EmployeeUpdate
import crud
from auth import create_token

# --------------------
# APP INIT
# --------------------
app = FastAPI(title="RedSecOps API")

# --------------------
# CORS
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# DATABASE INIT
# --------------------
Base.metadata.create_all(bind=engine)

# --------------------
# DEPENDENCY
# --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------
# ROOT
# --------------------
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

# --------------------
# AUTH
# --------------------
@app.post("/login")
def login(data: dict):
    # simple demo login
    if data.get("email") and data.get("password"):
        return {
            "token": create_token(data["email"])
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

# --------------------
# EMPLOYEE ROUTES
# --------------------
@app.get("/api/employees")
def get_employees(db: Session = Depends(get_db)):
    return crud.get_all_employees(db)

@app.post("/api/employees")
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

@app.put("/api/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.update_employee(db, employee_id, employee)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

# --------------------
# FILE UPLOAD
# --------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-dp")
def upload_profile_image(file: UploadFile = File(...)):
    filename = file.filename.replace(" ", "_")
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "file_url": f"/uploads/{filename}"
    }
