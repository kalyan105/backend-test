from sqlalchemy import Column, Integer, String
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    email = Column(String, unique=True)
    country_code = Column(String)
    mobile = Column(String)
    department = Column(String)
    lpa = Column(String)
    experience = Column(String)
    avatar_url = Column(String, nullable=True)
