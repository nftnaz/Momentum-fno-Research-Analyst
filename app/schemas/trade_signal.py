from enum import Enum
from typing import Optional

from pydantic import BaseModel


# ---------------------------------------------------------
# ENUMS
# ---------------------------------------------------------

class SignalType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class TradeType(str, Enum):
    BTST = "BTST"
    STBT = "STBT"
    SWING = "SWING"
    INTRADAY = "INTRADAY"


class MarketRegime(str, Enum):
    BULLISH_TREND = "BULLISH_TREND"
    BEARISH_TREND = "BEARISH_TREND"
    SIDEWAYS_VOLATILE = "SIDEWAYS_VOLATILE"
    BREAKOUT_FAVORABLE = "BREAKOUT_FAVORABLE"


class SignalStatus(str, Enum):
    ACTIVE = "ACTIVE"
    TARGET_1_HIT = "TARGET_1_HIT"
    TARGET_2_HIT = "TARGET_2_HIT"
    SL_HIT = "SL_HIT"
    CLOSED = "CLOSED"


# ---------------------------------------------------------
# TRADE SIGNAL
# ---------------------------------------------------------

class TradeSignal(BaseModel):

    id: str

    symbol: str

    stockName: str

    sector: str

    signalType: SignalType

    tradeType: TradeType

    setupCategory: str

    timestamp: str

    entryPrice: float

    stopLoss: float

    target1: float

    target2: float

    riskRewardRatio: str

    winProbability: float

    confidenceScore: float

    expectedReturnPercent: float

    expectedDrawdownPercent: float

    suggestedCapitalAllocation: float

    suggestedSharesOrLots: str

    riskPerTradeAmount: float

    status: SignalStatus

    entryReasonTechnical: str

    entryReasonML: str

    regime: MarketRegime

    telegramSent: bool = False

    telegramSentAt: Optional[str] = None