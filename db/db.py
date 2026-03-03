"""
Подключение к БД
"""

import logging

from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from enviroment import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

logger.debug("ПОДКЛЮЧЕНИЕ К БД " + DB_URL)
logger.debug("ПОДКЛЮЧЕНИЕ К БД " + DB_URL)

engine = create_engine(DB_URL, echo=True)

inspector = inspect(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    tables = inspector.get_table_names()
    logger.debug('ТАБЛИЦЫ ДО ' + str(tables))
    Base.metadata.create_all(bind=engine)
    logger.debug('ТАБЛИЦЫ ПОСЛЕ ' + str(tables))
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
