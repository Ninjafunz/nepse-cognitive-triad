"""Local Historical CSV Loader for Free Offline Backtesting.
Bypasses paid APIs by reading historical OHLCV data directly from CSV files.
"""

from typing import List, Dict, Any
import csv
from datetime import datetime


class HistoricalCSVLoader:
    """Loads historical OHLCV CSV data into standardized dictionary bars for the Triad."""

    @staticmethod
    def load_csv(file_path: str, symbol: str = "NABIL") -> List[Dict[str, Any]]:
        """Reads a CSV file containing date, open, high, low, close, volume."""
        bars = []
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            prev_close = None
            for row in reader:
                # Support multiple header casings (Date/date, Close/close, etc.)
                date_str = row.get("Date") or row.get("date") or row.get("time")
                open_val = float(row.get("Open") or row.get("open") or 0.0)
                high_val = float(row.get("High") or row.get("high") or 0.0)
                low_val = float(row.get("Low") or row.get("low") or 0.0)
                close_val = float(row.get("Close") or row.get("close") or 0.0)
                vol_val = float(row.get("Volume") or row.get("volume") or 0.0)

                if prev_close is None:
                    prev_close = open_val

                try:
                    dt = datetime.fromisoformat(date_str)
                except Exception:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")

                bars.append({
                    "timestamp": dt,
                    "symbol": symbol,
                    "open": open_val,
                    "high": high_val,
                    "low": low_val,
                    "close": close_val,
                    "prev_close": prev_close,
                    "volume": vol_val,
                    "time": dt.isoformat(),
                })
                prev_close = close_val

        return bars


csv_loader = HistoricalCSVLoader()
