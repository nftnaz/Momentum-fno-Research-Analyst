from app.core.config import settings


class TelegramService:
    async def send_message(self, text: str) -> dict:
        """
        Placeholder: no real HTTP call until TELEGRAM_ENABLED and credentials are set.
        """
        if not settings.TELEGRAM_ENABLED:
            return {
                "ok": False,
                "skipped": True,
                "reason": "Telegram disabled (TELEGRAM_ENABLED=false)",
            }

        if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
            return {
                "ok": False,
                "skipped": True,
                "reason": "Telegram credentials missing in .env",
            }

        # Later: real call
        # url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        # payload = {"chat_id": settings.TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
        return {
            "ok": False,
            "skipped": True,
            "reason": "Telegram send not implemented yet (placeholder)",
        }

    async def send_signal_alert(self, signal: dict) -> dict:
        text = (
            f"{signal.get('signalType', 'SIGNAL')} {signal.get('symbol', '')}\n"
            f"Entry: {signal.get('entryPrice')}\n"
            f"SL: {signal.get('stopLoss')} | T1: {signal.get('target1')}"
        )
        return await self.send_message(text)


telegram_service = TelegramService()