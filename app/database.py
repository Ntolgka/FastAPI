from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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


# Below code is connection to database without sqlalchemy orm. If you want to use regular sql queries.
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', database='fastapi', user='postgres', password='password123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()  # to execute sql statements
#         print("Connected to database")
#         break
#     except Exception as error:
#         print("Connection to database failed dur to:", error)
#         time.sleep(5)
