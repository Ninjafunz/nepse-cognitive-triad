# Zero-Cost Local Setup & Verification Guide

This project is engineered to run 100% locally on your machine with **zero cloud costs, zero paid API keys, and zero paid LLM tokens**.

---

## 1. The Zero-Cost Architecture

| Layer | Component | Zero-Cost Technology |
|---|---|---|
| **Logic & Computation** | Technical indicators, Triad consensus, T+2 calendar | Python 3.12 (Standard Library + Polars) |
| **Local AI Brain** | Autonomous literature-grounded strategic audit memos | **Ollama** running `llama3:8b` on local CPU/GPU (with deterministic fallback) |
| **Data Ingestion** | Historical OHLCV market replay | Local CSV reader (`csv_loader.py`) |
| **Database & Cache** | Time-series hypertable, T+2 ledger, and vector store | **Docker Desktop** (`timescaledb-ha:pg16` + Redis Alpine) |
| **Mission Control UI** | Real-time consensus cards, AI consciousness, risk guards | Browser-based UI on `http://localhost:3000` |

---

## 2. Step-by-Step Setup

### Step 1: Launch the Local AI Brain (Ollama)
1. Download and install **Ollama** from [ollama.com](https://ollama.com).
2. Open your terminal and run:
   ```bash
   ollama run llama3
   ```
3. Your local Ollama server will listen at `http://localhost:11434`. The Cognitive Triad automatically connects to this endpoint to draft strategic memos. If Ollama is offline, the system seamlessly uses its built-in literature-grounded audit engine.

---

### Step 2: Launch the Local Database (Docker Desktop)
When Docker Desktop is installed, start the TimescaleDB + pgvector container:
```bash
docker compose up -d db redis
```
This boots a PostgreSQL 16 instance with:
- `timescaledb` extension for 1-minute OHLCV candles
- `vector` (pgvector) extension for 1536-dimensional academic embeddings
- `redis` container for task scheduling

---

### Step 3: Run Free Local Historical CSV Backtests
No paid NEPSE subscription or live broker API is required. You can load and replay local CSVs directly:

```powershell
cd apps\backend

# 1. Generate 100-row sample historical CSV datasets (NABIL & SHIVM)
python generate_sample_csv.py

# 2. Run the CSV backtester using the local Triad consensus
python run_csv_backtest.py
```

**Expected Output:**
```
===========================================================================
NEPSE COGNITIVE TRIAD: LOCAL CSV BACKTEST RUNNER (NABIL)
Zero-Cost Architecture: Local File Ingestion & Deterministic Execution
===========================================================================
[*] Loaded 100 historical bars from nabil_historical_100.csv
Starting Capital           : NPR 13,300,000.00 ($100k USD)
Ending Portfolio Equity    : NPR 16,459,742.79
Cumulative Return          : +23.76%
Max Drawdown               : 0.54%
Total Completed Trades     : 1
Total Friction Fees Paid   : NPR 10,362.32
---------------------------------------------------------------------------

[SAMPLE LOCAL AI STRATEGIC MEMO GENERATED]
### Strategic Audit Memo: BUY NABIL

**Consensus Score**: +41.75/100 (Alpha: 70.0 | Beta: 25.0 | Gamma: 20.0)

Route Alpha signals positive structural conditions, aligning with Hyman Minsky's
hedge-finance phase and Keynesian liquidity preference. Simultaneously, Route Beta
registers retail narrative acceleration per Robert Shiller's Narrative Economics...
```

---

## 3. Launch the Local Dashboard & API

Double-click [`start_services.bat`](../start_services.bat) or run:

```powershell
# Start API Server on port 8000
python server.py

# Start Mission Control on port 3000
python ui_server.py
```

- **Mission Control UI:** [http://localhost:3000](http://localhost:3000)
- **OpenAPI Interactive Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
