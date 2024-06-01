from pymongo import MongoClient, errors as pymongo_errors
from dotenv import load_dotenv
from pathlib import Path
import os
import sys
from pydantic import BaseModel
from bunnet import Document, init_bunnet
from typing import Optional, List
from datetime import datetime


class Address(BaseModel):
    houseNumber: str
    streetName: str
    city: str
    state: str
    zipcode: str

# This is the model that will be saved to the database


class Show(Document):
    venueName: str
    timezone: Optional[str] = "America/New York",
    fbLink: Optional[str] = None,
    address: Address
    startTime: datetime
    endTime: Optional[datetime] = None,
    entryTime: Optional[datetime] = None,
    otherBands: Optional[List[str]] = []

    class Settings:
        name = "wotb_shows"


def get_database():
    try:
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        dotenv_path = Path(".env")
        load_dotenv(dotenv_path=dotenv_path)
        CONN_STRING = os.getenv("CONN_STRING")
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONN_STRING)
        # Create the database for our example (we will use the same database throughout the tutorial
        print(client.list_database_names())
        init_bunnet(database=client.wotb, document_models=[Show])
        shows = Show.all().run()
        for show in shows:
            # This does not give a very readable output
            print(show.venueName)
            print("\n")

        return client['wotb']
    except pymongo_errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":

    # Get the database
    dbname = get_database()
