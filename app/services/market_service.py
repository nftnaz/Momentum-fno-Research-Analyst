import httpx
from datetime import datetime

from fastapi import HTTPException

from app.core.config import settings

from app.schemas.market import (
    MarketBreadth,
    MarketStatus,
    MarketRegime,
)


class MarketService:

    def __init__(self):
        self.base_url = settings.UPSTOX_BASE_URL.rstrip("/")
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.UPSTOX_ACCESS_TOKEN}",
        }

    # ---------------------------------------------------
    # Dashboard Market Breadth (live indices)
    # ---------------------------------------------------

    async def get_market_breadth(self) -> MarketBreadth:
        """
        Live Nifty / Bank Nifty quotes via Upstox.
        advances/declines stay mocked until you compute them.
        """
        fallback = MarketBreadth(
            advances=1180,
            declines=945,
            unchanged=105,
            nifty50Price=25120.45,
            nifty50ChangePercent=0.82,
            bankNiftyPrice=56312.90,
            bankNiftyChangePercent=1.14,
            regime=MarketRegime.BULLISH_TREND,
        )

        try:
            nifty_q = await self.get_market_quote("NSE_INDEX|Nifty 50")
            bank_q = await self.get_market_quote("NSE_INDEX|Nifty Bank")

            n_price = float(nifty_q.get("last_price") or fallback.nifty50Price)
            n_chg = float(nifty_q.get("change") or 0)
            n_pct = float(
                nifty_q.get("change_percent")
                if nifty_q.get("change_percent") is not None
                else ((n_chg / n_price * 100) if n_price else 0)
            )

            b_price = float(bank_q.get("last_price") or fallback.bankNiftyPrice)
            b_chg = float(bank_q.get("change") or 0)
            b_pct = float(
                bank_q.get("change_percent")
                if bank_q.get("change_percent") is not None
                else ((b_chg / b_price * 100) if b_price else 0)
            )

            return MarketBreadth(
                advances=fallback.advances,
                declines=fallback.declines,
                unchanged=fallback.unchanged,
                nifty50Price=round(n_price, 2),
                nifty50ChangePercent=round(n_pct, 2),
                bankNiftyPrice=round(b_price, 2),
                bankNiftyChangePercent=round(b_pct, 2),
                regime=MarketRegime.BULLISH_TREND,
            )
        except Exception as e:
            print(f"get_market_breadth fallback: {e}")
            return fallback

    # ---------------------------------------------------
    # Optional market status helper (not used by /status route)
    # ---------------------------------------------------

    def get_market_status(self) -> MarketStatus:
        now = datetime.now()
        return MarketStatus(
            marketOpen=True,
            marketName="NSE",
            exchange="NSE",
            currentTime=now.isoformat(),
            tradingSession="REGULAR",
            message="Market status (static helper)",
        )

    # ---------------------------------------------------
    # Live Quote
    # ---------------------------------------------------

    async def get_market_quote(self, instrument_key: str):
        url = f"{self.base_url}/v2/market-quote/quotes"
        params = {"instrument_key": instrument_key}

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                url,
                headers=self.headers,
                params=params,
            )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Upstox API error: {e.response.text}",
            )

        data = response.json()

        print("\n========================================")
        print("Instrument Key:", instrument_key)
        print("Upstox Response:")
        print(data)
        print("========================================\n")

        if data.get("status") != "success" or not data.get("data"):
            raise HTTPException(
                status_code=502,
                detail=f"No quote returned for {instrument_key}",
            )

        # Upstox returns dynamic keys such as NSE_EQ:TCS
        quote = next(iter(data["data"].values()))

        last_price = float(quote.get("last_price", 0) or 0)
        change = float(quote.get("net_change", 0) or 0)
        previous_close = last_price - change

        if previous_close != 0:
            change_percent = round((change / previous_close) * 100, 2)
        else:
            change_percent = 0.0

        return {
            "symbol": quote.get("symbol"),
            "last_price": last_price,
            "volume": quote.get("volume"),
            "change": change,
            "change_percent": change_percent,
            "timestamp": quote.get("timestamp"),
        }

    # ---------------------------------------------------
    # Historical Candles
    # ---------------------------------------------------

    async def get_historical_candles(
        self,
        instrument_key: str,
        unit: str,
        interval: int,
        from_date: str,
        to_date: str,
    ):
        url = (
            f"{self.base_url}"
            f"/v3/historical-candle/"
            f"{instrument_key}"
            f"/{unit}"
            f"/{interval}"
            f"/{to_date}"
            f"/{from_date}"
        )

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                url,
                headers=self.headers,
            )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Upstox API error: {e.response.text}",
            )

        data = response.json()
        candles = []

        if (
            data.get("status") == "success"
            and "data" in data
            and "candles" in data["data"]
        ):
            for candle in reversed(data["data"]["candles"]):
                candles.append(
                    {
                        "time": candle[0],
                        "open": candle[1],
                        "high": candle[2],
                        "low": candle[3],
                        "close": candle[4],
                        "volume": candle[5],
                    }
                )

        return candles

    # ---------------------------------------------------
    # Multiple Stock History
    # ---------------------------------------------------

    async def get_stock_history(
        self,
        stocks,
        unit,
        interval,
        from_date,
        to_date,
    ):
        results = {}

        for stock in stocks:
            candles = await self.get_historical_candles(
                instrument_key=stock["instrument_key"],
                unit=unit,
                interval=interval,
                from_date=from_date,
                to_date=to_date,
            )
            results[stock["symbol"]] = candles

        return results


market_service = MarketService()