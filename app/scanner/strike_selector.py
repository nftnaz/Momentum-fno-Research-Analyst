from datetime import datetime


class StrikeSelector:

    def select_atm_contracts(
        self,
        option_data: list,
        spot_price: float,
    ):

        if not option_data:
            return None

        today = datetime.today().date()

        monthly = []

        for item in option_data:

            expiry = datetime.strptime(
                item["expiry"],
                "%Y-%m-%d"
            ).date()

            if not item["weekly"]:
                monthly.append(item)

        if not monthly:
            monthly = option_data

        # -----------------------------
        # Monthly rollover
        # -----------------------------

        if today.day >= 25:

            expiries = sorted(
                list(
                    {
                        x["expiry"]
                        for x in monthly
                    }
                )
            )

            if len(expiries) > 1:

                selected_expiry = expiries[1]

            else:

                selected_expiry = expiries[0]

        else:

            selected_expiry = sorted(
                {
                    x["expiry"]
                    for x in monthly
                }
            )[0]

        contracts = [

            x for x in monthly

            if x["expiry"] == selected_expiry

        ]

        ce = [
            x for x in contracts
            if x["instrument_type"] == "CE"
        ]

        pe = [
            x for x in contracts
            if x["instrument_type"] == "PE"
        ]

        if not ce or not pe:
            return None

        ce_contract = min(
            ce,
            key=lambda x: abs(
                x["strike_price"] - spot_price
            ),
        )

        pe_contract = min(
            pe,
            key=lambda x: abs(
                x["strike_price"] - spot_price
            ),
        )

        return {

            "expiry": selected_expiry,

            "ce": ce_contract,

            "pe": pe_contract,

        }


strike_selector = StrikeSelector()