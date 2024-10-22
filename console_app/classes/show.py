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
    notes: Optional[str] = None
    notesEmbedding: Optional[List[float]] = None

    def to_dict(self):
        """Convert the Show object to a dictionary for serialization."""
        return {
            "venueName": self.venueName,
            "timezone": self.timezone,
            "fbLink": self.fbLink,
            # Assuming Address class has a to_dict method
            "address": self.address.to_dict() if self.address else None,
            "startTime": self.startTime.isoformat() if self.startTime else None,
            "endTime": self.endTime.isoformat() if self.endTime else None,
            "entryTime": self.entryTime.isoformat() if self.entryTime else None,
            "otherBands": self.otherBands,
            "payout": self.payout,
            "notes": self.notes,
            "notesEmbedding": self.notesEmbedding
        }

    class Settings:
        name = "wotb_shows"

    @staticmethod
    def get_properties_and_types():
        properties = get_type_hints(Show)
        result = []
        for prop, prop_type in properties.items():
            result.append(f"{prop}: {prop_type}")
        return "\n".join(result)

    @staticmethod
    def get_properties() -> list[str]:
        properties = get_type_hints(Show)
        result = []
        for prop, prop_type in properties.items():
            result.append(f"{prop}")
        return result
