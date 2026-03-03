"""
Подключение к БД
"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from enviroment import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


class Base(DeclarativeBase):
    pass


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

logger.debug("ПОДКЛЮЧЕНИЕ К БД" + DB_URL)

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Создает таблицу, если её нет"""
    try:
        # Проверяем, есть ли таблица
        from sqlalchemy import inspect
        inspector = inspect(engine)

        if not inspector.has_table("tabletest"):
            logger.debug("Создаем таблицу tabletest...")
            Base.metadata.create_all(bind=engine)
            logger.debug("Таблица создана!")
        else:
            logger.debug("Таблица уже существует")
    except Exception as e:
        logger.debug(f"Ошибка при проверке/создании таблицы: {e}")


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
