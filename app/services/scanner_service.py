from app.scanner.scanner_engine import scanner_engine
from app.data.universe import load_fno_universe, load_all_stocks


class ScannerService:

    async def run_scan(self, category: str = "FNO"):
        """
        Scan FnO / equity universe.

        category:
          - FNO          → preferred liquid FnO list (load_fno_universe)
          - ALL          → full stocks.json (can be slow)
          - NIFTY50 etc. → same preferred list for now (extend later)
        """

        if category and category.upper() == "ALL":
            stocks = load_all_stocks()
        else:
            # Default: liquid FnO-style universe
            stocks = load_fno_universe()

        # Ensure exchange field exists for engine compatibility
        normalized = []
        for s in stocks:
            item = dict(s)
            if "exchange" not in item or not item["exchange"]:
                item["exchange"] = "NSE_EQ"
            # stocks.json uses "NSE" — engine only needs instrument_key
            if item.get("exchange") == "NSE":
                item["exchange"] = "NSE_EQ"
            normalized.append(item)

        result = await scanner_engine.scan_market(
            stocks=normalized,
            unit="minutes",
            interval=3,
        )

        return result


scanner_service = ScannerService()