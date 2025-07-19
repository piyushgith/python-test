from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from employee import Employee, get_db_connection, EMPLOYEE_NOT_FOUND_MESSAGE
from datetime import datetime
from typing import List, Dict, Optional
import sqlite3
import json

app = FastAPI()

@app.post("/employees/", response_model=Employee)
async def create_employee(employee: Employee):
    if employee.id is not None:
        raise HTTPException(status_code=400, detail="ID should not be provided for new employees")
    if employee.startDate > datetime.now().date():
        raise HTTPException(status_code=400, detail="Start date cannot be in the future")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO employees (name, email, position, startDate, endDate) VALUES (?, ?, ?, ?, ?)",
            (employee.name, employee.email, employee.position, employee.startDate.isoformat(), employee.endDate.isoformat() if employee.endDate else None)
        )
        conn.commit()
        employee.id = cursor.lastrowid
        return employee
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        conn.close()

@app.get("/employees/", response_model=List[Employee])
async def get_all_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees_data = cursor.fetchall()
    conn.close()
    return [Employee(**dict(emp)) for emp in employees_data]

@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    employee_data = cursor.fetchone()
    conn.close()
    if employee_data is None:
        raise HTTPException(status_code=404, detail=EMPLOYEE_NOT_FOUND_MESSAGE)
    return Employee(**dict(employee_data))

@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, employee: Employee):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    existing_employee = cursor.fetchone()
    if existing_employee is None:
        conn.close()
        raise HTTPException(status_code=404, detail=EMPLOYEE_NOT_FOUND_MESSAGE)

    try:
        cursor.execute(
            "UPDATE employees SET name = ?, email = ?, position = ?, startDate = ?, endDate = ? WHERE id = ?",
            (employee.name, employee.email, employee.position, employee.startDate.isoformat(), employee.endDate.isoformat() if employee.endDate else None, employee_id)
        )
        conn.commit()
        employee.id = employee_id
        return employee
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        conn.close()

@app.delete("/employees/delete_all", response_model=Dict[str, str])
async def delete_all_employees():
    conn = get_db_connection()
    cursor = conn.cursor()
    try: # SQLite does not support TRUNCATE. Use DELETE FROM instead.
        cursor.execute("DELETE FROM employees")
        #Reset the auto-increment counter
        cursor.execute("delete from sqlite_sequence where name='employees'")
        conn.commit()
        return {"message": "All employees deleted successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@app.delete("/employees/{employee_id}", response_model=Dict[str, str])
async def delete_employee(employee_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail=EMPLOYEE_NOT_FOUND_MESSAGE)
    return {"message": "Employee deleted successfully"}        


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
