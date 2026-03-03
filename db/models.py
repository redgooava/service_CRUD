"""
Моделька для БД
"""


from sqlalchemy import Column, Integer, String, Numeric

from db import Base


class Tabletest(Base):
    __tablename__ = "tabletest"
    db_id = Column(Integer, primary_key=True)
    rate_id = Column(Integer)
    rate_name = Column(String(50))
    service_id = Column(Integer)
    service_name = Column(String(50))
    price = Column(Numeric(14, 4))
