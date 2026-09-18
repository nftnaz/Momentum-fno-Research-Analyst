from datetime import datetime

from app.services.scanner_service import scanner_service
from app.services.instrument_service import instrument_service

from app.schemas.trade_signal import (
    TradeSignal,
    SignalType,
    TradeType,
    SignalStatus,
    MarketRegime,
)


class SignalService:


    def _get_signal_strength(self, score: int):

        if score >= 80:
            return "STRONG MOMENTUM"

        elif score >= 60:
            return "MODERATE MOMENTUM"

        elif score >= 40:
            return "WATCHLIST"

        else:
            return "WEAK"


    def _get_regime(self, score: int):

        if score >= 70:

            return MarketRegime.BULLISH_TREND


        elif score >= 50:

            return MarketRegime.BREAKOUT_FAVORABLE


        else:

            return MarketRegime.SIDEWAYS_VOLATILE



    async def get_all_signals(self):


        scan_result = await scanner_service.run_scan()


        signals = []


        for stock in scan_result["stocks"]:


            instrument = instrument_service.get_by_symbol(
                stock["symbol"]
            )


            stock_name = (
                instrument["name"]
                if instrument
                else stock["symbol"]
            )


            price = float(
                stock["last_price"]
            )


            score = int(
                stock["score"]
            )


            signal_strength = self._get_signal_strength(
                score
            )


            stop_loss = round(
                price * 0.98,
                2
            )


            target1 = round(
                price * 1.03,
                2
            )


            target2 = round(
                price * 1.06,
                2
            )



            signal = TradeSignal(


                id=f"SIG-{stock['symbol']}",


                symbol=stock["symbol"],


                stockName=stock_name,


                sector="Unknown",


                signalType=SignalType.BUY,


                tradeType=TradeType.BTST,


                setupCategory="Momentum Scanner",


                timestamp=datetime.now().isoformat(),


                entryPrice=price,


                stopLoss=stop_loss,


                target1=target1,


                target2=target2,


                riskRewardRatio="1:2",


                winProbability=min(
                    score,
                    95
                ),


                confidenceScore=score,


                expectedReturnPercent=6.0,


                expectedDrawdownPercent=2.0,


                suggestedCapitalAllocation=100000,


                suggestedSharesOrLots=(
                    f"{int(100000 / price)} Shares"
                ),


                riskPerTradeAmount=2000,


                status=SignalStatus.ACTIVE,


                entryReasonTechnical=(
                    f"Momentum Score = {score} | "
                    f"Signal = {signal_strength}"
                ),


                entryReasonML=(
                    "Momentum Scanner Engine"
                ),


                regime=self._get_regime(
                    score
                ),


                telegramSent=False,


                telegramSentAt=None,


            )


            signals.append(signal)



        return signals




    async def get_signal(
        self,
        symbol: str
    ):


        signals = await self.get_all_signals()


        for signal in signals:


            if signal.symbol.upper() == symbol.upper():

                return signal



        return None




    async def generate_signal(
        self,
        symbol: str
    ):


        return await self.get_signal(symbol)




    async def mark_telegram_sent(
        self,
        signal_id: str
    ):


        signals = await self.get_all_signals()


        for signal in signals:


            if signal.id == signal_id:


                signal.telegramSent = True


                signal.telegramSentAt = (
                    datetime.now().isoformat()
                )


                return signal



        return None




signal_service = SignalService()