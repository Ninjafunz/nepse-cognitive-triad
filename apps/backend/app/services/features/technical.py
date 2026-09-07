"""Technical Indicator Feature Engineering using Polars and pure-math fallbacks.
Computes indicators for Route Alpha (momentum, trends) and Route Beta (overbought/oversold, volatility).
"""

from typing import List, Dict, Any, Union
import math

try:
    import polars as pl
    HAS_POLARS = True
except ImportError:
    HAS_POLARS = False


class TechnicalFeatureEngine:
    """Computes technical indicators for the Cognitive Triad."""

    @staticmethod
    def compute_all(df_or_dicts: Union[Any, List[Dict[str, Any]]]) -> Any:
        if HAS_POLARS and isinstance(df_or_dicts, pl.DataFrame):
            return TechnicalFeatureEngine._compute_polars(df_or_dicts)
        else:
            return TechnicalFeatureEngine._compute_dicts(df_or_dicts)

    @staticmethod
    def _compute_polars(df: "pl.DataFrame") -> "pl.DataFrame":
        df = df.with_columns([
            TechnicalFeatureEngine._rsi(pl.col("close"), window=14).alias("rsi_14"),
            TechnicalFeatureEngine._ema(pl.col("close"), span=20).alias("ema_20"),
            TechnicalFeatureEngine._ema(pl.col("close"), span=50).alias("ema_50"),
            TechnicalFeatureEngine._bollinger_width(pl.col("close"), window=20).alias("bb_width_20"),
            pl.col("close").pct_change().rolling_std(window=20).alias("volatility_20"),
            pl.col("volume").rolling_mean(window=20).alias("volume_sma_20"),
            (pl.col("volume") / (pl.col("volume").rolling_mean(window=20) + 1e-9)).alias("volume_ratio"),
            (pl.col("high") - pl.col("low")).alias("candle_range"),
            ((pl.col("close") - pl.col("low")) / (pl.col("high") - pl.col("low") + 1e-9)).alias("candle_position"),
        ])

        df = df.with_columns([
            (pl.col("ema_20") > pl.col("ema_50")).cast(pl.Int8).alias("trend_bullish"),
            (pl.col("volume_ratio") > 1.5).cast(pl.Int8).alias("volume_spike"),
        ])
        return df

    @staticmethod
    def _rsi(series: "pl.Expr", window: int = 14) -> "pl.Expr":
        delta = series.diff()
        gain = delta.clip(lower_bound=0).rolling_mean(window=window)
        loss = (-delta.clip(upper_bound=0)).rolling_mean(window=window)
        rs = gain / (loss + 1e-9)
        return 100 - (100 / (1 + rs))

    @staticmethod
    def _ema(series: "pl.Expr", span: int) -> "pl.Expr":
        return series.ewm_mean(span=span)

    @staticmethod
    def _bollinger_width(series: "pl.Expr", window: int = 20) -> "pl.Expr":
        sma = series.rolling_mean(window=window)
        std = series.rolling_std(window=window)
        upper = sma + 2 * std
        lower = sma - 2 * std
        return (upper - lower) / (sma + 1e-9)

    @staticmethod
    def _compute_dicts(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Accurate fallback calculation for testing / environments without Polars."""
        if not rows:
            return []

        closes = [float(r["close"]) for r in rows]
        volumes = [float(r.get("volume", 0.0)) for r in rows]
        n = len(rows)

        def calc_ema(values, span):
            alpha = 2.0 / (span + 1.0)
            ema = [values[0]]
            for val in values[1:]:
                ema.append(alpha * val + (1.0 - alpha) * ema[-1])
            return ema

        ema_20 = calc_ema(closes, 20)
        ema_50 = calc_ema(closes, 50)

        # RSI 14
        rsi_14 = [50.0] * n
        if n >= 15:
            gains, losses = [], []
            for i in range(1, n):
                diff = closes[i] - closes[i - 1]
                gains.append(max(0.0, diff))
                losses.append(max(0.0, -diff))

            for i in range(14, n):
                window_gains = gains[i - 14:i]
                window_losses = losses[i - 14:i]
                avg_gain = sum(window_gains) / 14.0
                avg_loss = sum(window_losses) / 14.0
                rs = avg_gain / (avg_loss + 1e-9)
                rsi_val = 100.0 - (100.0 / (1.0 + rs))
                rsi_14[i] = round(rsi_val, 2)

        enriched = []
        for i, row in enumerate(rows):
            r = dict(row)
            r["rsi_14"] = rsi_14[i]
            r["ema_20"] = round(ema_20[i], 2)
            r["ema_50"] = round(ema_50[i], 2)

            if i >= 20:
                pct_changes = [(closes[k] - closes[k - 1]) / closes[k - 1] for k in range(i - 19, i + 1)]
                mean_pct = sum(pct_changes) / len(pct_changes)
                var = sum((p - mean_pct) ** 2 for p in pct_changes) / len(pct_changes)
                r["volatility_20"] = round(math.sqrt(var), 4)

                vol_window = volumes[i - 19:i + 1]
                vol_sma = sum(vol_window) / 20.0
                r["volume_sma_20"] = vol_sma
                r["volume_ratio"] = round(r.get("volume", 0.0) / (vol_sma + 1e-9), 2)
            else:
                r["volatility_20"] = 0.015
                r["volume_sma_20"] = r.get("volume", 1000.0)
                r["volume_ratio"] = 1.0

            high = float(r.get("high", r["close"]))
            low = float(r.get("low", r["close"]))
            close = float(r["close"])
            candle_range = high - low
            r["candle_range"] = candle_range
            r["candle_position"] = round((close - low) / (candle_range + 1e-9), 2)

            # Shorter span EMA reacts faster; in a rising series EMA20 > EMA50
            r["trend_bullish"] = 1 if r["ema_20"] > r["ema_50"] else 0
            r["volume_spike"] = 1 if r["volume_ratio"] > 1.5 else 0

            enriched.append(r)

        return enriched
