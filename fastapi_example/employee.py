from pydantic import BaseModel
from datetime import date
from typing import List, Dict, Optional
import sqlite3


EMPLOYEE_NOT_FOUND_MESSAGE = "Employee not found"

class Employee(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    position: str
    startDate: date
    endDate: Optional[date] = None

def get_db_connection():
    conn = sqlite3.connect('employees.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            position TEXT NOT NULL,
            startDate TEXT NOT NULL,
            endDate TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database table when the application starts
create_table()