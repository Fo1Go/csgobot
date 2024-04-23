from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine import URL, create_engine
from sqlalchemy.orm import sessionmaker

url = URL.create(drivername='postgresql+psycopg2',
                 username="postgres",
                 password="postgres",
                 host="localhost",
                 port=5432,
                 database="postgres")
engine = create_engine(url)
connection = engine.connect()


class Base(DeclarativeBase):
    ...


maker = sessionmaker(bind=engine)
session = maker()
