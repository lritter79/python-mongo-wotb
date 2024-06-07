from pydantic import BaseModel, Field
from pymongo import errors as pymongo_errors
from dotenv import load_dotenv
from pathlib import Path
import os
import sys
from beanie import init_beanie
from classes import Show
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient


async def mongo_client_wrapper(func):
    try:
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        dotenv_path = Path(".env")
        load_dotenv(dotenv_path=dotenv_path)
        CONN_STRING = os.getenv("CONN_STRING")
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        print("Open Connection")
        client = AsyncIOMotorClient(CONN_STRING)

        async def wrapper(*args, **kwds):
            return await func(*args, **kwds)
        results = await wrapper(client)
        client.close()
        print("Connection Closed")
        return results
    except pymongo_errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)


async def get_next_show():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        query = {"startTime": {"$gt": datetime.today()}}
        shows = await Show.find(query).sort("startTime").limit(1).to_list()
        if shows.__len__() > 0:
            return shows[0]
        return None
    return await mongo_client_wrapper(call_client)


async def get_all_upcoming_shows():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        query = {"startTime": {"$gt": datetime.today()}}
        shows = await Show.find_many(query).to_list()
        return shows
    return await mongo_client_wrapper(call_client)


async def get_all_shows():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        shows = await Show.find_all().to_list()
        return shows
    return await mongo_client_wrapper(call_client)


async def get_most_recent_show():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        query = {"startTime": {"$lt": datetime.today()}}
        shows = await Show.find(query).sort("-startTime").limit(1).to_list()
        if shows.__len__() > 0:
            return shows[0]
        return None
    return await mongo_client_wrapper(call_client)


async def get_highest_show_payout():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        query = {"payout": {"$exists": True, "$ne": None}}
        payout = await Show.find(query).sort("-payout").limit(1).to_list()
        return payout[0].payout
    return await mongo_client_wrapper(call_client)

# aggregate methods


class OutputItem(BaseModel):
    id: str = Field(None, alias="_id")
    value: float


async def get_total_show_payout():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        query = {"payout": {"$exists": True, "$ne": None}}
        payout = await Show.find(query).sum(Show.payout)
        return payout
    return await mongo_client_wrapper(call_client)


async def get_average_show_payout():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        query = {"payout": {"$exists": True, "$ne": None}}
        payout = await Show.find(query).aggregate(
            [{"$group": {"_id": {"$toString": "$_id"}, "value": {"$avg": "$payout"}}}],
            projection_model=OutputItem
        ).to_list()
        return payout[0].value
    return await mongo_client_wrapper(call_client)

# Intsert method


async def add_show(**kwargs):
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        show = Show(kwargs)
        doc = await Show.insert_one(show)
        return doc
    return await mongo_client_wrapper(call_client)
