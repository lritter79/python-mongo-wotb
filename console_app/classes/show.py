from beanie import Document
from typing import Optional, List, get_type_hints
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

    @staticmethod
    def get_properties_and_types():
        properties = get_type_hints(Show)
        result = []
        for prop, prop_type in properties.items():
            result.append(f"{prop}: {prop_type}")
        return "\n".join(result)
