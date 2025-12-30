from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    role: str
    email: str
    country_code: str = "+91"
    mobile: str
    department: str
    lpa: str
    experience: str
    avatar_url: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None
    country_code: Optional[str] = None
    mobile: Optional[str] = None
    department: Optional[str] = None
    lpa: Optional[str] = None
    experience: Optional[str] = None
    avatar_url: Optional[str] = None

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
