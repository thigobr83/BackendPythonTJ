from fastapi import FastAPI, Request, Cookie, Response
from typing import List, Optional
import time
from odmantic import ObjectId

from model.client import Client
from util.config import Configuration
from util.database import Database


config = Configuration()
logger = config.get_logger()
database = Database(config.get_db_url(), config.get_db_name())

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    logger.info(f"client {request.client.host}:{request.client.port}")
    process_time = time.time() - start_time
    logger.info(f"time response >> {process_time}")
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/client", response_model=List[Client], response_model_exclude={"user"})
async def client_list():
    result = await database.engine.find(Client)
    return result


@app.get("/client/{client_id}", response_model=Client, response_model_exclude={"user"})
async def get_client(client_id: ObjectId):
    logger.info(client_id)
    client = await database.engine.find_one(Client, Client.id == client_id)
    return client


@app.post("/client/", response_model=Client, response_model_exclude={"user"})
async def new_client(client: Client):
    await database.engine.save(client)
    return client


@app.put("/client/{client_id}", response_model=Client, response_model_exclude={"user"})
async def update_client(client_id: ObjectId, client: Client):
    try:
        c = await database.engine.find_one(Client, Client.id == client_id)
        logger.info(client.dict(exclude={"id"}))
        c.update_fields(client)
        await database.engine.save(c)
    except Exception as e:
        logger.exception(e)
    return c


@app.delete("/client/{client_id}")
async def delete_client(client_id: ObjectId):
    try:
        client = await database.engine.find_one(Client, Client.id == client_id)
        await database.engine.delete(client)
    except Exception as e:
        logger.exception(e)
    return {"message": client_id}


@app.get("/cookie")
def get_cookie(name: Optional[str] = Cookie(None)):
    return {"cookie": name}


@app.post("/cookie/{name}")
def create_cookie(name: str, response: Response):
    response.set_cookie(key="name", value=name)
    return {"message": "Welcome to the dark side, we have cookies"}
