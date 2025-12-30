# Redsecops Employee Management System - Database Setup

## Database Configuration

The system now uses **SQLite** with **SQLAlchemy** ORM for persistent employee data storage.

### Files Created:

1. **database.py** - Database connection and session management
2. **models.py** - Employee SQLAlchemy model
3. **schemas.py** - Pydantic schemas for API requests/responses
4. **crud.py** - CRUD operations for employee data
5. **init_db.py** - Database initialization script with sample data

### Database Location:
- `backend/redsecops.db` (SQLite database file)

## API Endpoints

### Get All Employees
```bash
GET http://127.0.0.1:8000/api/employees
```
Returns all employees from the database.

### Get Single Employee
```bash
GET http://127.0.0.1:8000/api/employees/{id}
```
Returns a specific employee by ID.

### Create New Employee
```bash
POST http://127.0.0.1:8000/api/employees
Content-Type: application/json

{
  "name": "John Doe",
  "role": "Developer",
  "email": "john@example.com",
  "country_code": "+1",
  "mobile": "1234567890",
  "department": "Engineering",
  "lpa": "₹15.0 LPA",
  "experience": "3 Years",
  "avatar_url": "https://..."
}
```

### Update Employee
```bash
PUT http://127.0.0.1:8000/api/employees/{id}
Content-Type: application/json

{
  "name": "Updated Name",
  "mobile": "9999999999",
  "department": "Product"
}
```

### Delete Employee
```bash
DELETE http://127.0.0.1:8000/api/employees/{id}
```

## Sample Data

10 employees are pre-loaded in the database:
1. Rajesh Kumar - Senior Developer (Engineering)
2. Priya Sharma - Product Manager (Product)
3. Arjun Patel - DevOps Engineer (Infrastructure)
4. Neha Singh - UX/UI Designer (Design)
5. Vikram Singh - Data Scientist (AI/ML)
6. Anjali Patel - QA Lead (Quality Assurance)
7. Rohit Verma - Backend Developer (Engineering)
8. Sneha Das - Frontend Developer (Engineering)
9. Aditya Kumar - Cloud Architect (Cloud Services)
10. Meera Singh - HR Manager (Human Resources)

## Initialization

To reinitialize the database with sample data:
```bash
cd backend
python init_db.py
```

## Database Schema

### Employee Table
- id (Integer, Primary Key)
- name (String)
- role (String)
- email (String, Unique)
- country_code (String)
- mobile (String)
- department (String)
- lpa (String)
- experience (String)
- avatar_url (String, Optional)
