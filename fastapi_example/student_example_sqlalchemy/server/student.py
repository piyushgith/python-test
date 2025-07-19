from typing import Generator
from sqlalchemy import Column, Integer, String, create_engine, CheckConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database URL configuration
DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Student table
class Student(Base):
    """
    SQLAlchemy model for the students table.
    
    Attributes:
        id (int): Primary key
        name (str): Student's full name (max 100 chars)
        age (int): Student's age
        email (str): Student's email address (max 120 chars, must contain @)
    """
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    age = Column(Integer, CheckConstraint('age >= 0 AND age <= 120'))
    email = Column(String(120), unique=True, index=True, nullable=False)

# Dependency to get DB session
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy session.
    
    Yields:
        Session: SQLAlchemy database session
        
    Note:
        The session is automatically closed after the request is processed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the database tables
Base.metadata.create_all(bind=engine)    