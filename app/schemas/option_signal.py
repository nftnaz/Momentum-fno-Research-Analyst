from pydantic import BaseModel
from enum import Enum
from typing import Optional


class OptionType(str, Enum):

    CE = "CE"
    PE = "PE"



class OptionSignal(BaseModel):

    id: str

    symbol: str

    direction: str

    optionType: OptionType

    strikePrice: float

    expiry: str

    optionPrice: float

    confidenceScore: float

    signal: str

    reason: str

    status: str
