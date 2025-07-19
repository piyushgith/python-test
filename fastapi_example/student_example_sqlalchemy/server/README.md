
# Student Example (SQLAlchemy)

This folder demonstrates how to build a simple REST API for managing student records using FastAPI and SQLAlchemy.

## Contents

- `student_server.py`: FastAPI server exposing endpoints to interact with student data.
- `student.py`: SQLAlchemy models and database logic for student records.

## Features

- Add, update, delete, and retrieve student records via API endpoints.
- Uses SQLite as the database backend.
- Demonstrates integration of FastAPI with SQLAlchemy ORM.

## Usage

1. Install dependencies:
   ```
   pip install fastapi uvicorn sqlalchemy
   ```
2. Run the server:
   ```
   uvicorn student_server:app --reload
   ```
3. Access the API docs at `http://127.0.0.1:8000/docs`.

This example is intended for learning and demonstration purposes.
