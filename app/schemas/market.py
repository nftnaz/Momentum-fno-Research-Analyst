from enum import Enum

from pydantic import BaseModel


# ---------------------------------------------------------
# MARKET REGIME
# ---------------------------------------------------------

class MarketRegime(str, Enum):

    BULLISH_TREND = "BULLISH_TREND"

    BEARISH_TREND = "BEARISH_TREND"

    SIDEWAYS_VOLATILE = "SIDEWAYS_VOLATILE"

    BREAKOUT_FAVORABLE = "BREAKOUT_FAVORABLE"


# ---------------------------------------------------------
# MARKET BREADTH
# ---------------------------------------------------------

class MarketBreadth(BaseModel):

    advances: int

    declines: int

    unchanged: int

    nifty50Price: float

    nifty50ChangePercent: float

    bankNiftyPrice: float

    bankNiftyChangePercent: float

    regime: MarketRegime


# ---------------------------------------------------------
# MARKET STATUS
# ---------------------------------------------------------

class MarketStatus(BaseModel):

    marketOpen: bool

    marketName: str

    exchange: str

    currentTime: str

    tradingSession: str

    message: str