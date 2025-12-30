from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import jwt
import os
import sys
from datetime import datetime, timedelta
from fastapi import File, UploadFile
import base64
from sqlalchemy.orm import Session

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import engine, get_db, Base
from models import Employee as EmployeeModel
from schemas import EmployeeCreate, EmployeeUpdate, Employee as EmployeeSchema
import crud

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS (required for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend directory at /static so browsers can load the HTML file
from fastapi.staticfiles import StaticFiles
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
if os.path.isdir(frontend_dir):
    app.mount('/static', StaticFiles(directory=frontend_dir), name='static')

SECRET_KEY = os.getenv("SECRET_KEY", "secret123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_current_user(request: Request) -> str:
    """Verify JWT token from Authorization header and return user email"""
    auth_header = request.headers.get("authorization", "")
    
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    # Handle both "Bearer token" and "bearer token"
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = parts[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"status": "backend running"}

@app.get("/login", response_class=HTMLResponse)
async def get_login():
    return """
    <html>
      <body>
        <h2>Login</h2>
        <form method="post" action="/login">
          <input name="email" placeholder="email" /><br/>
          <input name="password" type="password" placeholder="password" /><br/>
          <button type="submit">Login</button>
        </form>
      </body>
    </html>
    """

@app.post("/login")
async def login(request: Request, email: str = Form(None), password: str = Form(None)):
    content_type = request.headers.get("content-type", "")
    if content_type.startswith("application/json"):
        body = await request.json()
        email = body.get("email")
        password = body.get("password")

    if email == "admin@example.com" and password == "admin123":
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode(
            {"sub": email, "exp": int(expire.timestamp())},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        return {"token": token}

    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/upload-dp")
async def upload_display_picture(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload employee display picture"""
    try:
        # Verify token
        email = verify_token(request)
        
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Get employee_id from form data
        form = await request.form()
        employee_id = form.get("employee_id")
        
        if not employee_id:
            raise HTTPException(status_code=400, detail="employee_id is required")
        
        # Read file content
        content = await file.read()
        
        # Convert to base64 for storage/transmission
        encoded_image = base64.b64encode(content).decode("utf-8")
        
        # Create data URI
        file_url = f"data:{file.content_type};base64,{encoded_image}"
        
        # Update employee avatar in database
        employee = crud.get_employee(db, int(employee_id))
        if employee:
            employee.avatar_url = file_url
            db.add(employee)
            db.commit()
            db.refresh(employee)
        
        return JSONResponse({
            "success": True,
            "file_url": file_url,
            "message": "Profile picture uploaded successfully"
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# ============ EMPLOYEE API ENDPOINTS ============

@app.get("/api/employees", response_model=list[EmployeeSchema])
async def get_all_employees(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all employees"""
    employees = crud.get_all_employees(db)
    return employees

@app.get("/api/employees/{employee_id}", response_model=EmployeeSchema)
async def get_employee(employee_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get specific employee"""
    employee = crud.get_employee(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.post("/api/employees", response_model=EmployeeSchema)
async def create_employee(employee: EmployeeCreate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create new employee"""
    # Check if email already exists
    existing = crud.get_employee_by_email(db, employee.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_employee(db, employee)

@app.put("/api/employees/{employee_id}", response_model=EmployeeSchema)
async def update_employee(employee_id: int, employee: EmployeeUpdate, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update employee"""
    updated = crud.update_employee(db, employee_id, employee)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@app.delete("/api/employees/{employee_id}")
async def delete_employee(employee_id: int, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete employee"""
    deleted = crud.delete_employee(db, employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return JSONResponse({"detail": "Employee deleted successfully"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
