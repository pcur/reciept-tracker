from dataclasses import dataclass
from typing import List

@dataclass
class Item:
    name: str
    price: float

@dataclass
class Receipt:
    id: int
    store: str
    date: str  # You can change this to `datetime.date` if parsing dates
    total: float
    payment_type: str
    items: List[Item]
    image_url: str
