from app.services.instrument_search_service import instrument_search_service
from app.services.option_quote_service import option_quote_service
from app.scanner.strike_selector import strike_selector


class OptionChainService:
    """
    Live ATM CE/PE premiums from Upstox instrument search + quotes.
    """

    def _normalize_contracts(self, search_payload: dict) -> list:
        """
        Flatten Upstox search response into list of dicts for StrikeSelector.
        """
        raw = search_payload.get("data") or search_payload
        if isinstance(raw, dict):
            items = (
                raw.get("instruments")
                or raw.get("data")
                or raw.get("docs")
                or []
            )
        elif isinstance(raw, list):
            items = raw
        else:
            items = []

        contracts = []
        for item in items:
            if not isinstance(item, dict):
                continue

            strike = item.get("strike_price") or item.get("strike")
            opt_type = (
                item.get("instrument_type")
                or item.get("option_type")
                or item.get("type")
            )
            expiry = item.get("expiry") or item.get("expiry_date")
            key = item.get("instrument_key")

            if strike is None or not opt_type or not expiry or not key:
                continue

            opt_type = str(opt_type).upper()
            if opt_type not in ("CE", "PE"):
                if "CE" in opt_type or opt_type == "CALL":
                    opt_type = "CE"
                elif "PE" in opt_type or opt_type == "PUT":
                    opt_type = "PE"
                else:
                    continue

            contracts.append(
                {
                    "strike_price": float(strike),
                    "instrument_type": opt_type,
                    "expiry": str(expiry)[:10],
                    "instrument_key": key,
                    "trading_symbol": item.get("trading_symbol")
                    or item.get("tradingsymbol")
                    or "",
                    "lot_size": item.get("lot_size") or item.get("lot") or 1,
                    "weekly": bool(item.get("weekly", False)),
                }
            )
        return contracts

    async def get_atm_premiums(self, symbol: str, spot_price: float) -> dict | None:
        try:
            search = await instrument_search_service.get_option_contracts(symbol)
            contracts = self._normalize_contracts(search)
            if not contracts:
                print(f"get_atm_premiums({symbol}): no contracts")
                return None

            atm = strike_selector.select_atm_contracts(contracts, spot_price)
            if not atm:
                print(f"get_atm_premiums({symbol}): ATM not found")
                return None

            ce = atm["ce"]
            pe = atm["pe"]

            ce_q = await option_quote_service.get_quote(ce["instrument_key"])
            pe_q = await option_quote_service.get_quote(pe["instrument_key"])

            if not ce_q and not pe_q:
                print(f"get_atm_premiums({symbol}): no quotes")
                return None

            return {
                "atm_strike": float(ce["strike_price"]),
                "expiry": atm["expiry"],
                "atmCePremium": float(ce_q["last_price"]) if ce_q and ce_q.get("last_price") is not None else None,
                "atmPePremium": float(pe_q["last_price"]) if pe_q and pe_q.get("last_price") is not None else None,
                "ce_instrument_key": ce["instrument_key"],
                "pe_instrument_key": pe["instrument_key"],
                "ce_trading_symbol": ce.get("trading_symbol"),
                "pe_trading_symbol": pe.get("trading_symbol"),
                "lot_size": ce.get("lot_size") or pe.get("lot_size") or 1,
            }
        except Exception as e:
            print(f"get_atm_premiums({symbol}) failed: {e}")
            return None

    async def enrich_scan_rows(
        self,
        stocks: list,
        high_score: float = 60,
        low_score: float = 40,
        max_enrich: int = 25,
    ) -> list:
        """
        Attach live ATM CE/PE to strong (CE) and weak (PE) names.
        Budget is split so PE is not starved by many high-score names.
        """
        if not stocks:
            return []

        # Split candidates
        high = sorted(
            [s for s in stocks if float(s.get("score") or 0) >= high_score],
            key=lambda x: float(x.get("score") or 0),
            reverse=True,
        )
        low = sorted(
            [s for s in stocks if float(s.get("score") or 0) <= low_score],
            key=lambda x: float(x.get("score") or 0),  # weakest first
        )

        # Reserve roughly half the budget for each side
        half = max(1, max_enrich // 2)
        to_enrich_symbols = set()

        for s in high[:half]:
            sym = s.get("symbol")
            if sym:
                to_enrich_symbols.add(str(sym).upper())

        for s in low[:half]:
            sym = s.get("symbol")
            if sym:
                to_enrich_symbols.add(str(sym).upper())

        # If budget left, fill from remaining high then low
        remaining = max_enrich - len(to_enrich_symbols)
        if remaining > 0:
            for s in high[half:] + low[half:]:
                if remaining <= 0:
                    break
                sym = s.get("symbol")
                if not sym:
                    continue
                key = str(sym).upper()
                if key not in to_enrich_symbols:
                    to_enrich_symbols.add(key)
                    remaining -= 1

        print(
            f"Enriching {len(to_enrich_symbols)} symbols "
            f"(high>={high_score}: {len(high)}, low<={low_score}: {len(low)})"
        )

        enriched = []
        for row in stocks:
            item = dict(row)
            symbol = str(item.get("symbol") or "").upper()
            spot = float(item.get("last_price") or 0)

            if symbol in to_enrich_symbols and spot > 0:
                atm = await self.get_atm_premiums(symbol, spot)
                if atm:
                    item.update(atm)
                    print(
                        f"  {symbol}: strike={atm.get('atm_strike')} "
                        f"CE={atm.get('atmCePremium')} PE={atm.get('atmPePremium')}"
                    )
                else:
                    print(f"  {symbol}: ATM enrich failed")

            enriched.append(item)

        return enriched


option_chain_service = OptionChainService()