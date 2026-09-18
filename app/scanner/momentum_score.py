from app.scanner.filters import (
    bullish_ema_crossover,
    volume_confirmation,
    is_price_above_ema
)



def calculate_momentum_score(
    candles
):

    score = 0


    # Trend
    if bullish_ema_crossover(candles):
        score += 30


    # Price strength
    if is_price_above_ema(
        candles,
        30
    ):
        score += 25


    # Volume confirmation
    if volume_confirmation(candles):
        score += 20


    # Recent momentum
    if candles[-1]["close"] > candles[-5]["close"]:
        score += 15


    # Strong candle
    latest = candles[-1]

    body = (
        latest["close"]
        -
        latest["open"]
    )


    if body > 0:
        score += 10


    return min(score,100)