from pydantic import BaseModel
from typing import Optional


class EmployeeBase(BaseModel):
    name: str
    role: str
    email: str
    country_code: str
    mobile: str
    department: str
    lpa: str
    experience: str


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

