from pydantic import BaseModel


class Address(BaseModel):
    houseNumber: str
    streetName: str
    city: str
    state: str
    zipcode: str
