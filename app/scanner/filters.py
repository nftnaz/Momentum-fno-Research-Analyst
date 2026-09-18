from typing import List, Dict


def has_minimum_candles(
    candles: List[Dict],
    minimum: int = 50
) -> bool:

    return len(candles) >= minimum



def is_price_above_ema(
    candles: List[Dict],
    ema_period: int
) -> bool:

    closes = [
        candle["close"]
        for candle in candles
    ]

    if len(closes) < ema_period:
        return False


    ema = calculate_ema(
        closes,
        ema_period
    )


    return closes[-1] > ema[-1]



def calculate_ema(
    prices: List[float],
    period: int
):

    multiplier = 2 / (period + 1)

    ema = []

    ema.append(prices[0])


    for price in prices[1:]:

        value = (
            price * multiplier
            +
            ema[-1] * (1 - multiplier)
        )

        ema.append(value)


    return ema



def volume_confirmation(
    candles: List[Dict],
    lookback: int = 20
):

    if len(candles) < lookback:
        return False


    recent_volume = candles[-1]["volume"]


    avg_volume = sum(
        c["volume"]
        for c in candles[-lookback:]
    ) / lookback


    return recent_volume > avg_volume



def bullish_ema_crossover(
    candles: List[Dict]
):

    closes = [
        c["close"]
        for c in candles
    ]


    ema10 = calculate_ema(
        closes,
        10
    )

    ema30 = calculate_ema(
        closes,
        30
    )


    return (
        ema10[-1] > ema30[-1]
    )