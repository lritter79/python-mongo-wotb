from beanie import Document
from typing import Optional, List
from datetime import datetime
from classes.address import Address


class Show(Document):
    venueName: str
    timezone: Optional[str] = "America/New York",
    fbLink: Optional[str] = None,
    address: Address
    startTime: datetime
    endTime: Optional[datetime] = None,
    entryTime: Optional[datetime] = None,
    otherBands: Optional[List[str]] = []
    payout: Optional[int] = None

    class Settings:
        name = "wotb_shows"
