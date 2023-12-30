from pydantic import BaseModel
from pydantic import Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []
