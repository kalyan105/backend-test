"""Initialize database with sample employee data"""
from database import SessionLocal, engine, Base
from models import Employee
import models

# Create all tables
Base.metadata.create_all(bind=engine)

# Sample employee data
employees_data = [
    {
        "name": "Rajesh Kumar",
        "role": "Senior Developer",
        "email": "rajesh@resecops.com",
        "country_code": "+91",
        "mobile": "9876543210",
        "department": "Engineering",
        "lpa": "₹18.5 LPA",
        "experience": "6 Years",
        "avatar_url": "https://i.pravatar.cc/150?img=1"
    },
    {
        "name": "Priya Sharma",
        "role": "Product Manager",
        "email": "priya@resecops.com",
        "country_code": "+91",
        "mobile": "9876543211",
        "department": "Product",
        "lpa": "₹16.0 LPA",
        "experience": "4 Years",
        "avatar_url": "https://i.pravatar.cc/150?img=2"
    },
    {
        "name": "Arjun Patel",
        "role": "DevOps Engineer",
        "email": "arjun@resecops.com",
        "country_code": "+91",
        "mobile": "9876543212",
        "department": "Infrastructure",
        "lpa": "₹15.5 LPA",
        "experience": "5 Years",
        "avatar_url": "https://i.pravatar.cc/150?img=3"
    },
    {
        "name": "Neha Singh",
        "role": "UX/UI Designer",
        "email": "neha@resecops.com",
        "country_code": "+91",
        "mobile": "9876543213",
        "department": "Design",
        "lpa": "₹12.0 LPA",
        "experience": "3 Years",
        "avatar_url": "https://i.pravatar.cc/150?img=4"
    },
    {
        "name": "Vikram Singh",
        "role": "Data Scientist",
        "email": "vikram@resecops.com",
        "country_code": "+91",
        "mobile": "9876543214",
        "department": "AI/ML",
        "lpa": "₹17.0 LPA",
        "experience": "4 Years",
        "avatar_url": "https://i.pravatar.cc/150?img=5"
    },
    {
        "name": "Anjali Patel",
        "role": "QA Lead",
        "email": "anjali@resecops.com",
        "country_code": "+91",
        "mobile": "9876543215",
        "department": "Quality Assurance",
        "lpa": "₹13.5 LPA",
        "experience": "3 Years",
        "avatar_url": "https://i.pravatar.cc/150?img=6"
    },
    {
        "name": "Rohit Verma",
        "role": "Backend Developer",
        "email": "rohit@resecops.com",
        "country_code": "+91",
        "mobile": "9876543216",
        "department": "Engineering",
        "lpa": "₹14.0 LPA",
        "experience": "2 Years",
        "avatar_url": "https://i.pravatar.cc/150?img=7"
    },
    {
        "name": "Sneha Das",
        "role": "Frontend Developer",
        "email": "sneha@resecops.com",
        "country_code": "+91",
        "mobile": "9876543217",
        "department": "Engineering",
        "lpa": "₹13.0 LPA",
        "experience": "2 Years",
        "avatar_url": "https://i.pravatar.cc/150?img=8"
    },
    {
        "name": "Aditya Kumar",
        "role": "Cloud Architect",
        "email": "aditya@resecops.com",
        "country_code": "+91",
        "mobile": "9876543218",
        "department": "Cloud Services",
        "lpa": "₹19.0 LPA",
        "experience": "7 Years",
        "avatar_url": "https://i.pravatar.cc/150?img=9"
    },
    {
        "name": "Meera Singh",
        "role": "HR Manager",
        "email": "meera@resecops.com",
        "country_code": "+91",
        "mobile": "9876543219",
        "department": "Human Resources",
        "lpa": "₹11.5 LPA",
        "experience": "5 Years",
        "avatar_url": "https://i.pravatar.cc/150?img=10"
    }
]

# Add employees to database
db = SessionLocal()

# Check if employees already exist
existing_count = db.query(Employee).count()
if existing_count == 0:
    for emp_data in employees_data:
        employee = Employee(**emp_data)
        db.add(employee)
    
    db.commit()
    print(f"✅ Successfully added {len(employees_data)} employees to database")
else:
    print(f"⚠️ Database already contains {existing_count} employees. Skipping initialization.")

db.close()
