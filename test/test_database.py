import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://eam:eam@127.0.0.1:5000/PostgreSQL"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_db_connection(db_session):
    result = db_session.execute(text("SELECT 1"))
    assert result.fetchone() == (1,)