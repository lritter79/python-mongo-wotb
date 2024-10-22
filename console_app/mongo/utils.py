from typing import List
from bson import json_util
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
from bson.json_util import dumps
from hugging_face.utils import generate_embedding


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


async def get_shows(limit=10, sort="startTime", query_property=None, query_comparison_operator=None, query_compare_date=None, query_compare_string=None, query_compare_number=None):
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        shows = []
        if query_property != None and query_comparison_operator != None:
            query = {}
            if query_compare_date != None:
                query = {query_property: {
                    query_comparison_operator: query_compare_date}}
            elif query_compare_string != None:
                query = {query_property: {
                    query_comparison_operator: query_compare_string}}
            elif query_compare_number != None:
                query = {query_property: {
                    query_comparison_operator: query_compare_number}}
            shows = await Show.find(query).sort(sort).limit(limit).to_list()
        else:
            shows = await Show.find_many().sort(sort).limit(limit).to_list()
        if shows.__len__() > 0:
            return shows[0]
        return None
    return await mongo_client_wrapper(call_client)


async def get_next_show():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        query = {"startTime": {"$gt": datetime.today()}}
        shows = await Show.find(query).sort("startTime").limit(1).to_list()
        if shows.__len__() > 0:
            return shows[0]
        return None
    return await mongo_client_wrapper(call_client)


async def get_all_upcoming_shows() -> List[Show]:
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        query = {"startTime": {"$gt": datetime.today()}}
        shows = await Show.find_many(query).to_list()
        return shows
    return await mongo_client_wrapper(call_client)


async def get_all_shows() -> List[Show]:
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        shows = await Show.find(query=None).to_list()
        return shows
    return await mongo_client_wrapper(call_client)


async def get_most_recent_show():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        shows = await Show.find({"startTime": {"$lt": datetime.today()}}, sort=["-startTime"], limit=1).to_list()
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


async def get_semantic_notes_search(search_string):
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        query = {"$vectorSearch": {
            "queryVector": generate_embedding(search_string),
            "path": "notesEmbedding",
            "numCandidates": 100,
            "limit": 4,
            "index": "NotesSemanticSearch",
        }
        }
        shows = await Show.find(query).sum(Show.payout)
        return shows
    return await mongo_client_wrapper(call_client)


async def get_total_show_payout():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        query = {"payout": {"$exists": True, "$ne": None}}
        payout = await Show.find(query).sum(Show.payout)
        return payout
    return await mongo_client_wrapper(call_client)


async def get_average_show_payout():
    payout = await ask_database_about_shows({"$group": {"_id": {"$toString": "$_id"}, "value": {"$avg": "$payout"}}}, {"payout": {"$exists": True, "$ne": None}})

    return payout[0].value


async def get_average_show_payout_by_state():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        query = {"payout": {"$exists": True, "$ne": None}}
        payout = await Show.find(query).aggregate(
            [{"$group": {"_id": "$address.state", "value": {"$avg": "$payout"}}}],
            projection_model=OutputItem
        ).to_list()
        return payout
    avgs = await mongo_client_wrapper(call_client)
    return dumps(avgs, default=json_util.default)


# Insert method


async def add_show(**kwargs):
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        show = Show(**kwargs)
        doc = await Show.insert_one(show)
        return doc
    return await mongo_client_wrapper(call_client)

# update methods


async def add_show_notes_vector_embeddings():
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        show = await Show.find_one({'notesEmbedding': {"$exists": False}})
        embedding = generate_embedding(show.notes)
        await show.set({Show.notesEmbedding: embedding})
    return await mongo_client_wrapper(call_client)


async def ask_database_about_shows(grouping=None, **query):
    async def call_client(client):
        await init_beanie(database=client.wotb, document_models=[Show])
        if grouping == None:
            shows = await Show.find(**query).to_list()
            return shows
        results = await Show.find(**query).aggregate(
            [grouping],
            projection_model=OutputItem
        ).to_list()

        return results
    return await mongo_client_wrapper(call_client)
