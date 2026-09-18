import asyncio
from datetime import datetime, timedelta

from app.services.market_service import market_service
from app.scanner.momentum_score import calculate_momentum_score
from app.scanner.filters import has_minimum_candles


class ScannerEngine:

    def __init__(self, concurrency: int = 5):
        # Limit parallel Upstox calls to avoid rate limits
        self.concurrency = concurrency

    async def _scan_one(
        self,
        stock: dict,
        unit: str,
        interval: int,
        from_date: str,
        to_date: str,
        semaphore: asyncio.Semaphore,
        stats: dict,
    ):
        async with semaphore:
            try:
                candles = await market_service.get_historical_candles(
                    instrument_key=stock["instrument_key"],
                    unit=unit,
                    interval=interval,
                    from_date=from_date,
                    to_date=to_date,
                )

                if not has_minimum_candles(candles):
                    stats["insufficient_candles"] += 1
                    return None

                score = calculate_momentum_score(candles)

                quote = await market_service.get_market_quote(
                    stock["instrument_key"]
                )

                # Upstox quote shape: data["NSE_EQ:SYMBOL"]["last_price"]
                live_price = None
                if isinstance(quote, dict):
                    if "last_price" in quote:
                        live_price = quote["last_price"]
                    else:
                        # sometimes nested under data key
                        inner = quote.get("data") or quote
                        if isinstance(inner, dict):
                            for v in inner.values():
                                if isinstance(v, dict) and "last_price" in v:
                                    live_price = v["last_price"]
                                    break

                if live_price is None:
                    # fallback from last candle close if available
                    live_price = candles[-1][4] if candles else 0

                stats["processed"] += 1

                return {
                    "symbol": stock["symbol"],
                    "score": score,
                    "last_price": float(live_price),
                }

            except Exception as e:
                stats["errors"] += 1
                return {
                    "symbol": stock.get("symbol", "?"),
                    "error": str(e),
                }

    async def scan_market(
        self,
        stocks,
        unit="minutes",
        interval=15,
        from_date=None,
        to_date=None,
    ):
        if from_date is None:
            from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        if to_date is None:
            to_date = datetime.now().strftime("%Y-%m-%d")

        stats = {
            "total": len(stocks),
            "processed": 0,
            "insufficient_candles": 0,
            "errors": 0,
        }

        semaphore = asyncio.Semaphore(self.concurrency)

        tasks = [
            self._scan_one(
                stock=stock,
                unit=unit,
                interval=interval,
                from_date=from_date,
                to_date=to_date,
                semaphore=semaphore,
                stats=stats,
            )
            for stock in stocks
        ]

        results = await asyncio.gather(*tasks)

        valid_results = [r for r in results if r and "score" in r]
        valid_results.sort(key=lambda x: x["score"], reverse=True)

        errors = [r for r in results if r and "error" in r]

        return {
            "stats": stats,
            "stocks": valid_results,
            "errors": errors,
        }


scanner_engine = ScannerEngine(concurrency=5)