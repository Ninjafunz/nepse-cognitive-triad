"""Generates sample 100-row historical NEPSE OHLCV datasets for NABIL and SHIVM.
Enables instant local backtesting with zero cost and zero network requirements.
"""

import os
import csv
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def generate_sample_csv(symbol: str, start_price: float, filename: str, rows: int = 100):
    path = os.path.join(DATA_DIR, filename)
    start_date = datetime(2021, 1, 3)
    curr_price = start_price

    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Open", "High", "Low", "Close", "Volume"])

        day_offset = 0
        written = 0
        while written < rows:
            dt = start_date + timedelta(days=day_offset)
            day_offset += 1
            if dt.weekday() in (4, 5):  # Skip Friday & Saturday in Nepal
                continue

            open_p = curr_price
            drift = 1.012 if written % 7 != 0 else 0.985
            close_p = round(open_p * drift, 2)
            high_p = round(max(open_p, close_p) * 1.015, 2)
            low_p = round(min(open_p, close_p) * 0.985, 2)
            vol = int(25000 + (written * 350))

            writer.writerow([dt.strftime("%Y-%m-%d"), open_p, high_p, low_p, close_p, vol])
            curr_price = close_p
            written += 1

    print(f"[+] Generated {rows} rows of OHLCV data at: {path}")


if __name__ == "__main__":
    generate_sample_csv("NABIL", 750.0, "nabil_historical_100.csv", rows=100)
    generate_sample_csv("SHIVM", 520.0, "shivm_historical_100.csv", rows=100)
