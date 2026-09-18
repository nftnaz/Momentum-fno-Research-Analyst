from __future__ import annotations

import pandas as pd
import numpy as np


class TechnicalScore:

    """
    Calculates a 0-100 technical score.

    Current Factors

    ✓ EMA Trend
    ✓ EMA Alignment
    ✓ RSI
    ✓ MACD
    ✓ Volume
    ✓ Price Breakout

    Later we will add

    - ADX
    - ATR Expansion
    - SuperTrend
    - VWAP
    - Option OI
    - PCR
    - AI Ranking
    """

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def score(self, candles: list):

        if len(candles) < 60:

            return {
                "score": 0,
                "direction": "NONE",
                "reasons": [
                    "Not enough candles"
                ]
            }

        df = pd.DataFrame(candles)

        df = df.astype(
            {
                "open": float,
                "high": float,
                "low": float,
                "close": float,
                "volume": float,
            }
        )

        df = self._add_indicators(df)

        last = df.iloc[-1]

        score = 0

        reasons = []

        # -----------------------------------------------------
        # EMA Trend
        # -----------------------------------------------------

        if last.ema20 > last.ema50:

            score += 20
            reasons.append(
                "EMA20 above EMA50"
            )

        else:

            score -= 20
            reasons.append(
                "EMA20 below EMA50"
            )

        # -----------------------------------------------------
        # Price above EMA20
        # -----------------------------------------------------

        if last.close > last.ema20:

            score += 10

            reasons.append(
                "Price above EMA20"
            )

        else:

            score -= 10

        # -----------------------------------------------------
        # RSI
        # -----------------------------------------------------

        if 55 <= last.rsi <= 70:

            score += 15

            reasons.append(
                "Healthy RSI"
            )

        elif last.rsi > 75:

            score -= 5

        elif last.rsi < 35:

            score -= 15

        # -----------------------------------------------------
        # MACD
        # -----------------------------------------------------

        if last.macd > last.signal:

            score += 15

            reasons.append(
                "MACD Bullish"
            )

        else:

            score -= 15

        # -----------------------------------------------------
        # Volume
        # -----------------------------------------------------

        if last.volume > last.volume_ma:

            score += 15

            reasons.append(
                "Volume Expansion"
            )

        # -----------------------------------------------------
        # Breakout
        # -----------------------------------------------------

        highest20 = df.high.tail(20).max()

        lowest20 = df.low.tail(20).min()

        if last.close >= highest20:

            score += 25

            reasons.append(
                "20 Candle Breakout"
            )

        elif last.close <= lowest20:

            score -= 25

            reasons.append(
                "20 Candle Breakdown"
            )

        # -----------------------------------------------------
        # Clamp
        # -----------------------------------------------------

        score = max(
            0,
            min(100, score + 50)
        )

        direction = "LONG"

        if score < 50:

            direction = "SHORT"

        return {

            "score": int(score),

            "direction": direction,

            "reasons": reasons

        }

    # ---------------------------------------------------------
    # Indicators
    # ---------------------------------------------------------

    def _add_indicators(
        self,
        df: pd.DataFrame
    ):

        df["ema20"] = (
            df.close
            .ewm(span=20)
            .mean()
        )

        df["ema50"] = (
            df.close
            .ewm(span=50)
            .mean()
        )

        delta = df.close.diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()

        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        df["rsi"] = 100 - (

            100 /

            (1 + rs)

        )

        ema12 = df.close.ewm(span=12).mean()

        ema26 = df.close.ewm(span=26).mean()

        df["macd"] = ema12 - ema26

        df["signal"] = (

            df["macd"]

            .ewm(span=9)

            .mean()

        )

        df["volume_ma"] = (

            df.volume

            .rolling(20)

            .mean()

        )

        return df


technical_score = TechnicalScore()