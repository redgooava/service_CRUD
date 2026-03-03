"""
API
"""

import logging
import time

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Depends

from schemas import DataPostRequest, DataPostResponse, DataGetResponse
from db.db import get_db, init_db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

init_db()

app = FastAPI()

@app.get("/data", response_model=DataGetResponse)
def get_data(db=Depends(get_db)):
    query = text('SELECT * FROM tabletest')
    result = db.execute(query)
    data = result.fetchall()

    formatted_data = []
    for row in data:
        formatted_data.append({
            "db_id": row[0],
            "rate_id": row[1],
            "rate_name": row[2],
            "service_id": row[3],
            "service_name": row[4],
            "price": row[5]
        })

    logger.debug(f"Полученные данные: {formatted_data}")
    return DataGetResponse(data=formatted_data)


@app.post("/data", response_model=DataPostResponse)
def set_data(data: DataPostRequest, db=Depends(get_db)):
    logger.debug(f"Получены данные: {data}")

    query = text("""
                 INSERT INTO tabletest (db_id, rate_id, rate_name, service_id, service_name, price)
                 VALUES (:db_id, :rate_id, :rate_name, :service_id, :service_name, :price)
                 """)

    try:
        db.execute(query, {
            "db_id": data.db_id,
            "rate_id": data.rate_id,
            "rate_name": data.rate_name,
            "service_id": data.service_id,
            "service_name": data.service_name,
            "price": data.price
        })
        db.commit()
    except IntegrityError as e:
        return DataPostResponse(message="Данные с таким ключом уже существуют")
    logger.debug(f"Данные успешно вставлены")
    return DataPostResponse(message="Данные успешно вставлены")
