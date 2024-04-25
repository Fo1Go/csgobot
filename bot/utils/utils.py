from bot.models import User
from bot.utils.db import session


def get_or_create_user(*args, telegram_id, **kwargs) -> User | None:
    user = session.query(User).filter(User.telegram_id == telegram_id).one_or_none()
    if user is None:
        user = User(telegram_id=telegram_id)
        session.add(user)
        session.commit()
    return user


def get_user_by_id(*args, telegram_id, **kwargs) -> User | None:
    return session.query(User).filter(User.telegram_id == telegram_id).one_or_none()


def yes_or_no(question: bool):
    return 'yes' if question else 'no'


def un_or_noting(question: bool):
    return 'un' if question else ''
