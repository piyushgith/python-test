from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from datetime import date, datetime
from typing import List, Dict, Optional

app = FastAPI()

# In-memory database for demonstration purposes
db: Dict[int, "Employee"] = {}
next_id = 1

EMPLOYEE_NOT_FOUND_MESSAGE = "Employee not found"

class Employee(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    position: str
    startDate: date = date.today()
    endDate: Optional[date] = None

@app.post("/employees/", response_model=Employee)
async def create_employee(employee: Employee):
    global next_id
    employee.id = next_id
    db[next_id] = employee
    next_id += 1
    return employee

@app.get("/employees/", response_model=List[Employee])
async def get_all_employees():
    return list(db.values())

@app.get("/employees/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int):
    if employee_id not in db:
        raise HTTPException(status_code=404, detail=EMPLOYEE_NOT_FOUND_MESSAGE)
    return db[employee_id]

@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, employee: Employee):
    if employee_id not in db:
        raise HTTPException(status_code=404, detail=EMPLOYEE_NOT_FOUND_MESSAGE)
    employee.id = employee_id
    db[employee_id] = employee
    return employee

@app.delete("/employees/{employee_id}", response_model=Dict[str, str])
async def delete_employee(employee_id: int):
    if employee_id not in db:
        raise HTTPException(status_code=404, detail=EMPLOYEE_NOT_FOUND_MESSAGE)
    del db[employee_id]
    return {"message": "Employee deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
