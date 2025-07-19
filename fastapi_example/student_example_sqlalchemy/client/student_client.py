import sys
import os

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(project_root)

from fastapi_example.student_example_sqlalchemy.model.student_req import StudentRead, StudentCreate
from generic_client import GenericAPIClient

class StudentClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.client = GenericAPIClient[StudentRead](f"{base_url}/students", StudentRead)

    def create_student(self, name: str, age: int, email: str) -> StudentRead:
        """Create a new student"""
        student_data = StudentCreate(name=name, age=age, email=email)
        return self.client.create(student_data.model_dump())

    def get_student(self, student_id: int) -> StudentRead:
        """Get a student by ID"""
        return self.client.read(student_id)

    def get_all_students(self, skip: int = 0, limit: int = 10) -> list[StudentRead]:
        """Get all students with pagination"""
        return self.client.read(params={"skip": skip, "limit": limit})

    def delete_student(self, student_id: int) -> bool:
        """Delete a student"""
        return self.client.delete(student_id)

# Example usage:
if __name__ == "__main__":
    # Create a client instance
    client = StudentClient()

    try:
        # Create a new student
        new_student = client.create_student("John Doe", 20, "john@example.com")
        print(f"Created student: {new_student}")

        # Get the student by ID
        student = client.get_student(new_student.id)
        print(f"Retrieved student: {student}")

        # Get all students
        students = client.get_all_students(skip=0, limit=10)
        print(f"All students: {students}")

        # Delete the student
        deleted = client.delete_student(new_student.id)
        print(f"Student deleted: {deleted}")

    except Exception as e:
        print(f"Error: {e}")
