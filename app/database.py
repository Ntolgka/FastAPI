from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection string = 'postgresql://<username>:<password>@<ip-address/hostname>/<database-name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password123@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To talk to the database, we need a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All the models will inherit from this base class
Base = declarative_base()

# Every time a request is made, a new session will be created, after request close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
