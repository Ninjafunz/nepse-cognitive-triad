"""FastAPI main application entry point."""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import market_data, portfolio, orders, triad
from app.services.data_ingestion.poller import market_poller
from app.services.data_ingestion.nepse_client import nepse_client
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start polling loop
    asyncio.create_task(market_poller.start())
    yield
    # Shutdown: Stop poller and close HTTP sessions
    await market_poller.stop()
    await nepse_client.close()


app = FastAPI(
    title="NEPSE Cognitive Triad AI Trader API",
    description="Multi-agent paper trading system grounded in literature and NEPSE market realities.",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for local Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(market_data.router, prefix="/api/v1/market", tags=["Market Data"])
app.include_router(portfolio.router, prefix="/api/v1/portfolio", tags=["Portfolio & Ledger"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Order Execution"])
app.include_router(triad.router, prefix="/api/v1/triad", tags=["Cognitive Triad & Journals"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "system": "NEPSE Cognitive Triad"}
