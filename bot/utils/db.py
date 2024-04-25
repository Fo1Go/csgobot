from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.engine import URL, create_engine
import os
from dotenv import load_dotenv


class Base(DeclarativeBase):
    ...


load_dotenv("env")
url = URL.create(drivername=os.getenv("POSTGRES_DRIVER_NAME"),
                 username=os.getenv("POSTGRES_USERNAME"),
                 password="postgres",
                 host=os.getenv("POSTGRES_HOST"),
                 port=os.getenv("POSTGRES_PORT"),
                 database=str(os.getenv("POSTGRES_DATABASE")))
engine = create_engine(url)
connection = engine.connect()

maker = sessionmaker(bind=engine)
session = maker()
