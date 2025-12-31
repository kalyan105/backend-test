from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import shutil

from database import SessionLocal, engine
from models import Base
from schemas import EmployeeCreate, EmployeeUpdate
import crud
from auth import create_token

# =====================================================
# APP INITIALIZATION
# =====================================================

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

# =====================================================
# CORS CONFIG
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# DATABASE SESSION
# =====================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================================================
# ROOT ROUTE
# =====================================================

@app.get("/")
def root():
    return {
        "message": "Backend is running 🚀",
        "status": "OK"
    }

# =====================================================
# AUTH
# =====================================================

@app.post("/login")
def login(data: dict):
    if data.get("email") == "admin@resecops.com" and data.get("password") == "admin123":
        return {"token": create_token(data["email"])}

    raise HTTPException(status_code=401, detail="Invalid credentials")

# =====================================================
# EMPLOYEE ROUTES
# =====================================================

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


# =====================================================
# IMAGE UPLOAD
# =====================================================

UPLOAD_DIR = "uploads/profiles"
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
