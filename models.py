from sqlalchemy import Column, Integer, String, Float
from database import Base

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    email = Column(String, unique=True, index=True)
    country_code = Column(String, default="+91")
    mobile = Column(String)
    department = Column(String)
    lpa = Column(String)
    experience = Column(String)
    avatar_url = Column(String, nullable=True)
