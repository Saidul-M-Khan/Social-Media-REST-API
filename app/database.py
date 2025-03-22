from sqlalchemy import create_engine  #* Creates an engine to interact with the database
from sqlalchemy.ext.declarative import declarative_base  #* Provides a base class for ORM models
from sqlalchemy.orm import sessionmaker  #* Manages sessions for database connections

#* Database connection URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost/FastAPI_SocialMedia'

#* Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#* Create a configured "SessionLocal" class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#* Base class for defining ORM models
Base = declarative_base()

#* Dependency to get a database session for requests
def get_db():
    db = SessionLocal()  #* Create a new database session
    try:
        yield db  #* Provide the session to the caller
    finally:
        db.close()  #* Close the session after use
