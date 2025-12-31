from pydantic import BaseModel

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

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
