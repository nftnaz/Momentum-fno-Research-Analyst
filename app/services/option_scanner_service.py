from datetime import datetime

from app.services.scanner_service import scanner_service
from app.services.instrument_search_service import (
    instrument_search_service,
)
from app.services.market_service import market_service
from app.scanner.strike_selector import strike_selector
from app.services.option_quote_service import (
    option_quote_service,
)
from app.scanner.technical_score import (
    technical_score,
)

class OptionScannerService:

    async def scan_options(self):

        scanner_result = await scanner_service.run_scan()

        option_signals = []

        for stock in scanner_result["stocks"]:

            symbol = stock["symbol"]

            try:

                print(f"\nScanning {symbol}")

                # ---------------------------------------
                # Find Equity Instrument
                # ---------------------------------------

                instrument = (
                    instrument_search_service.get_equity_by_symbol(
                        symbol
                    )
                )

                if instrument is None:
                    print("Instrument not found")
                    continue
                                # ---------------------------------------
                # Live Spot Quote
                # ---------------------------------------

                spot = await market_service.get_market_quote(
                    instrument["instrument_key"]
                )

                spot_price = float(
                    spot["last_price"]
                )

                # ---------------------------------------
                # Historical Candles
                # ---------------------------------------

                candles = await market_service.get_historical_candles(
                    instrument_key=instrument["instrument_key"],
                    unit="days",
                    interval=1,
                    from_date="2026-05-01",
                    to_date=datetime.now().strftime("%Y-%m-%d"),
                )

                if len(candles) < 50:
                    print("Not enough candles")
                    continue

                # ---------------------------------------
                # Technical Analysis
                # ---------------------------------------

                technical = technical_score.calculate(
                    candles=candles,
                    current_price=spot_price,
                )

                score = technical["score"]

                trend = technical["trend"]

                signal = technical["signal"]

                reasons = technical["reasons"]

                print(
                    f"{symbol} | "
                    f"Score={score} | "
                    f"Trend={trend} | "
                    f"Signal={signal}"
                )

                # ---------------------------------------
                # Search Monthly Option Contracts
                # ---------------------------------------

                contracts = await (
                    instrument_search_service
                    .search_option_contracts(symbol)
                )

                if not contracts:

                    print("No option contracts found")

                    continue

                 # ---------------------------------------
                # Select ATM Strike
                # ---------------------------------------

                atm = strike_selector.select_atm_contracts(
                    contracts=contracts,
                    spot_price=spot_price,
                )

                if atm is None:

                    print("ATM strike not found")

                    continue

                # ---------------------------------------
                # Live Option Quotes
                # ---------------------------------------

                ce_quote = await option_quote_service.get_quote(
                    atm["ce"]["instrument_key"]
                )

                pe_quote = await option_quote_service.get_quote(
                    atm["pe"]["instrument_key"]
                )

                # ---------------------------------------
                # Trade Decision Engine
                # ---------------------------------------

                direction = "NO TRADE"
                selected = None
                quote = None
                confidence = score

                if trend == "BULLISH":

                    if score >= 80:
                        direction = "BUY CE"
                        selected = atm["ce"]
                        quote = ce_quote
                        confidence = score + 10

                    elif score >= 60:
                        direction = "BUY CE"
                        selected = atm["ce"]
                        quote = ce_quote
                        confidence = score

                elif trend == "BEARISH":

                    if score >= 80:
                        direction = "BUY PE"
                        selected = atm["pe"]
                        quote = pe_quote
                        confidence = score + 10

                    elif score >= 60:
                        direction = "BUY PE"
                        selected = atm["pe"]
                        quote = pe_quote
                        confidence = score

                confidence = min(confidence, 100)

                if selected is None:
                    continue

                option_signals.append(

                    {

                        "symbol": symbol,

                        "technical_score": score,

                        "confidence": confidence,

                        "trend": trend,

                        "signal": direction,

                        "reason": reasons,

                        "spot_price": spot_price,

                        "expiry": atm["expiry"],

                        "strike": selected["strike_price"],

                        "option_type": selected["instrument_type"],

                        "trading_symbol": selected["trading_symbol"],

                        "instrument_key": selected["instrument_key"],

                        "lot_size": selected["lot_size"],

                        "option_price": quote["last_price"],

                        "volume": quote["volume"],

                        "change_percent": quote["change_percent"],

                        "change": quote["change"],

                        "timestamp": quote["timestamp"],

                    }

                )

            except Exception as e:

                print(f"{symbol} failed : {e}")

        option_signals.sort(
            key=lambda x: x["confidence"],
            reverse=True,
        )

        return {

            "status": "success",

            "count": len(option_signals),

            "top_intraday": option_signals[:3],

            "top_btst": option_signals[:5],

            "data": option_signals,

        }

option_scanner_service = OptionScannerService()