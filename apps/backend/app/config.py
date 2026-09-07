"""FastAPI application configuration via Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/nepse_triad",
        description="Async PostgreSQL connection string",
    )
    DATABASE_URL_SYNC: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/nepse_triad",
        description="Sync PostgreSQL connection string for Alembic migrations",
    )

    # Redis & Task Queue
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    CELERY_BROKER_URL: str = Field(default="redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = Field(default="redis://localhost:6379/0")

    # Capital & Trading Simulation
    # NPR 13,300,000 (~$100,000 USD equivalent at ~133 NPR/USD)
    INITIAL_VIRTUAL_CAPITAL_NPR: float = Field(default=13300000.0)
    MAX_PORTFOLIO_CONCENTRATION_PCT: float = Field(default=0.15)
    ENABLE_PAPER_TRADING: bool = Field(default=True)

    # NEPSE Trading Specifics
    NEPSE_MARKET_OPEN_HOUR: int = Field(default=11)
    NEPSE_MARKET_CLOSE_HOUR: int = Field(default=15)
    CIRCUIT_BREAKER_NORMAL_PCT: float = Field(default=0.10)
    CIRCUIT_BREAKER_SPECIAL_PCT: float = Field(default=0.15)
    BROKER_COMMISSION_PCT: float = Field(default=0.0037)
    SEBON_FEE_PCT: float = Field(default=0.00015)
    DP_CHARGE_NPR: float = Field(default=25.0)

    # Polling & Ingestion
    POLLING_INTERVAL_SECONDS: int = Field(default=5)
    STALE_DATA_THRESHOLD_SECONDS: int = Field(default=30)
    VERIFY_NEPSE_SSL: bool = Field(default=False)

    # LLM & RAG Configuration (Local Llama-3 by default)
    LLM_PROVIDER: str = Field(default="local_llama3")
    LOCAL_LLAMA3_API_BASE: str = Field(default="http://localhost:11434/v1")
    LOCAL_LLAMA3_MODEL_NAME: str = Field(default="llama3:70b")
    EMBEDDING_DIMENSION: int = Field(default=1536)


settings = Settings()
