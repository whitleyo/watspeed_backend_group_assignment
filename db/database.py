from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Replace with your actual database URL
DATABASE_URL = "postgresql://username:password@localhost:5432/cafe_watspeed"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a scoped session for thread safety
db_session = scoped_session(SessionLocal)

def get_session():
    """
    Returns a new SQLAlchemy session.
    """
    return db_session()

def init_db():
    """
    Initialize the database by creating all tables.
    """
    from app.domain import models  # Import your models here
    models.Base.metadata.create_all(bind=engine)
