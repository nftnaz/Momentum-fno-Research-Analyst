from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# --------------------------------------------------
# Route Imports
# --------------------------------------------------

from app.api.routes.health_routes import router as health_router
from app.api.routes.market_routes import router as market_router
from app.api.routes.instrument_routes import router as instrument_router
from app.api.routes.scanner_routes import scanner_router
from app.api.routes.signal_routes import router as signal_router
from app.api.routes.settings_routes import router as settings_router
from app.api.routes.backtest_routes import router as backtest_router
from app.api.routes.papertrade_routes import router as papertrade_router
from app.api.routes.ai_routes import router as ai_router
from app.api.routes.fno_routes import router as fno_router
from app.api.routes.instrument_search_routes import ( router as instrument_search_router)
from app.api.routes.option_scanner_routes import router as option_scanner_router




# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


# --------------------------------------------------
# Middleware
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# API Routes
# --------------------------------------------------

# Health
app.include_router(
    health_router,
    prefix="/api",
    tags=["Health"]
)

# Market
app.include_router(
    market_router,
    prefix="/api/market",
    tags=["Market"]
)

# Instruments
app.include_router(
    instrument_router,
    prefix="/api/instruments",
    tags=["Instruments"]
)

# Scanner
app.include_router(
    scanner_router,
    prefix="/api/scanner",
    tags=["Scanner"]
)

# Signals
app.include_router(
    signal_router,
    prefix="/api/signals",
    tags=["Signals"]
)

# Settings
app.include_router(
    settings_router,
    prefix="/api/settings",
    tags=["Settings"]
)

# Backtesting
app.include_router(
    backtest_router,
    prefix="/api/backtest",
    tags=["Backtest"]
)

# Paper Trading
app.include_router(
    papertrade_router,
    prefix="/api/papertrade",
    tags=["Paper Trading"]
)

# AI Assistant
app.include_router(
    ai_router,
    prefix="/api/ai",
    tags=["AI Assistant"]
)

# FnO Universe
app.include_router(
    fno_router,
    prefix="/api/fno",
    tags=["FnO"]
)

app.include_router(
    instrument_search_router,
    prefix="/api/instrument-search",
    tags=["Instrument Search"]
)

app.include_router(
    option_scanner_router,
    prefix="/api/options",
    tags=["Options Scanner"]
)

# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
async def root():

    return {
        "message": "NSE AI Research Analyst Backend Running",
        "version": settings.APP_VERSION,
        "status": "healthy"
    }