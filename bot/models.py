from sqlalchemy import Column, Integer, Boolean, DateTime, Text
from bot.utils.db import Base


class User(Base):
    __tablename__ = 'bot_users'

    id = Column(Integer(), primary_key=True, unique=True)
    telegram_id = Column(Integer(), unique=True, nullable=False)
    subscribed_matches = Column(Boolean(), default=False)
    subscribed_updates = Column(Boolean(), default=False)
    subscribed_news = Column(Boolean(), default=False)

    def __repr__(self):
        return f'User({self.id}, {self.telegram_id})'


class Update(Base):
    __tablename__ = 'bot_updates'

    id = Column(Integer(), primary_key=True, unique=True)
    update_date = Column(DateTime(), nullable=False)
    update_url = Column(Text(), nullable=False)

    def __repr__(self):
        return f'Update({self.update_date}, {self.update_url})'
