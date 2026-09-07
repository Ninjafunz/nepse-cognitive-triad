"""High fidelity Event-Driven Backtesting Engine respecting all NEPSE market rules.
- T+2 settlement (cash from sells settles 2 working days later)
- No short selling
- Circuit breakers (reject orders outside +/- 10%)
- Broker commissions, SEBON fees, and DP charges
- Liquidity slippage
"""

from datetime import datetime, date
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
import math
from app.services.trading.slippage import fee_calculator
from app.services.settlement.t2_engine import t2_engine


@dataclass
class BacktestTrade:
    timestamp: datetime
    symbol: str
    side: str  # BUY or SELL only
    quantity: int
    price: float
    fees: float
    slippage: float
    pnl: float = 0.0


@dataclass
class BacktestResult:
    trades: List[BacktestTrade] = field(default_factory=list)
    equity_curve: List[float] = field(default_factory=list)
    total_return_pct: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown_pct: float = 0.0
    win_rate: float = 0.0
    total_fees_paid: float = 0.0
    total_trades: int = 0


class EventDrivenBacktester:
    """Simulates historic execution across bars with exact NEPSE settlement math."""

    def __init__(self, initial_capital: float = 13300000.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.pending_settlements: List[Dict[str, Any]] = []
        self.trades: List[BacktestTrade] = []
        self.equity_curve: List[float] = []

    def get_available_cash(self, current_date: date) -> float:
        """Returns cash that is already settled on or before current_date."""
        settled_credits = sum(
            s["amount"] for s in self.pending_settlements if s["settle_date"] <= current_date
        )
        return self.cash + settled_credits

    def check_circuit_breaker(self, ltp: float, prev_close: float) -> bool:
        """Enforces +/-10% price movement bands in NEPSE."""
        if prev_close <= 0:
            return True
        upper = prev_close * 1.10
        lower = prev_close * 0.90
        return lower <= ltp <= upper

    def execute_buy(
        self,
        timestamp: datetime,
        symbol: str,
        quantity: int,
        limit_price: float,
        prev_close: float,
        avg_volume: float = 25000.0,
    ) -> Optional[BacktestTrade]:
        if not self.check_circuit_breaker(limit_price, prev_close):
            return None

        slippage_pct = fee_calculator.estimate_slippage_pct(quantity, avg_volume)
        fill_price = fee_calculator.simulate_execution_price(limit_price, "BUY", slippage_pct)
        trade_val = fill_price * quantity
        fees_dict = fee_calculator.calculate_fees(trade_val, "BUY")
        total_cost = trade_val + fees_dict["total_fees"]

        available = self.get_available_cash(timestamp.date())
        if total_cost > available:
            return None  # Insufficient settled funds

        self.cash -= total_cost
        self._update_position(symbol, quantity, fill_price)

        trade = BacktestTrade(
            timestamp=timestamp,
            symbol=symbol,
            side="BUY",
            quantity=quantity,
            price=fill_price,
            fees=fees_dict["total_fees"],
            slippage=round(abs(fill_price - limit_price), 2),
        )
        self.trades.append(trade)
        return trade

    def execute_sell(
        self,
        timestamp: datetime,
        symbol: str,
        quantity: int,
        limit_price: float,
        prev_close: float,
        avg_volume: float = 25000.0,
    ) -> Optional[BacktestTrade]:
        if symbol not in self.positions or self.positions[symbol]["qty"] < quantity:
            return None  # No short selling allowed

        if not self.check_circuit_breaker(limit_price, prev_close):
            return None

        slippage_pct = fee_calculator.estimate_slippage_pct(quantity, avg_volume)
        fill_price = fee_calculator.simulate_execution_price(limit_price, "SELL", slippage_pct)
        trade_val = fill_price * quantity
        fees_dict = fee_calculator.calculate_fees(trade_val, "SELL")
        net_proceeds = trade_val - fees_dict["total_fees"]

        # T+2 Settlement progression
        settle_date = t2_engine.calculate_settlement_date(timestamp.date())
        self.pending_settlements.append({
            "amount": net_proceeds,
            "settle_date": settle_date,
            "origin_date": timestamp.date(),
        })

        cost_basis = self.positions[symbol]["avg_price"]
        pnl = (fill_price - cost_basis) * quantity - fees_dict["total_fees"]

        self._update_position(symbol, -quantity, fill_price)

        trade = BacktestTrade(
            timestamp=timestamp,
            symbol=symbol,
            side="SELL",
            quantity=quantity,
            price=fill_price,
            fees=fees_dict["total_fees"],
            slippage=round(abs(fill_price - limit_price), 2),
            pnl=round(pnl, 2),
        )
        self.trades.append(trade)
        return trade

    def _update_position(self, symbol: str, qty_change: int, price: float):
        if symbol not in self.positions:
            self.positions[symbol] = {"qty": 0, "avg_price": 0.0}
        pos = self.positions[symbol]
        if qty_change > 0:
            total_cost = (pos["qty"] * pos["avg_price"]) + (qty_change * price)
            pos["qty"] += qty_change
            pos["avg_price"] = round(total_cost / pos["qty"], 2) if pos["qty"] > 0 else 0.0
        else:
            pos["qty"] += qty_change
            if pos["qty"] <= 0:
                del self.positions[symbol]

    def _calculate_total_equity(self, current_prices: Dict[str, float]) -> float:
        pos_value = sum(
            p["qty"] * current_prices.get(sym, p["avg_price"])
            for sym, p in self.positions.items()
        )
        pending_credits = sum(s["amount"] for s in self.pending_settlements)
        return self.cash + pending_credits + pos_value

    def run(self, strategy_fn: Callable, bars: List[Dict[str, Any]]) -> BacktestResult:
        """Feeds time-ordered historical bars sequentially into strategy function."""
        current_prices: Dict[str, float] = {}

        for bar in bars:
            ts = bar["timestamp"]
            sym = bar["symbol"]
            close = float(bar["close"])
            prev_close = float(bar.get("prev_close", close))
            current_prices[sym] = close

            signal = strategy_fn(bar, self.positions, self.get_available_cash(ts.date()))
            if signal:
                if signal.get("action") == "BUY":
                    self.execute_buy(
                        timestamp=ts,
                        symbol=signal["symbol"],
                        quantity=signal["quantity"],
                        limit_price=signal.get("limit_price", close),
                        prev_close=prev_close,
                    )
                elif signal.get("action") == "SELL":
                    self.execute_sell(
                        timestamp=ts,
                        symbol=signal["symbol"],
                        quantity=signal["quantity"],
                        limit_price=signal.get("limit_price", close),
                        prev_close=prev_close,
                    )

            self.equity_curve.append(round(self._calculate_total_equity(current_prices), 2))

        return self._compile_results()

    def _compile_results(self) -> BacktestResult:
        if not self.equity_curve:
            return BacktestResult()

        final_equity = self.equity_curve[-1]
        total_return_pct = round(((final_equity - self.initial_capital) / self.initial_capital) * 100.0, 2)
        total_fees = sum(t.fees for t in self.trades)

        # Win Rate
        closed_sells = [t for t in self.trades if t.side == "SELL"]
        wins = [t for t in closed_sells if t.pnl > 0]
        win_rate = round((len(wins) / len(closed_sells) * 100.0), 2) if closed_sells else 0.0

        # Max Drawdown
        peak = self.initial_capital
        max_dd = 0.0
        for eq in self.equity_curve:
            if eq > peak:
                peak = eq
            dd = (peak - eq) / peak if peak > 0 else 0.0
            if dd > max_dd:
                max_dd = dd

        # Sharpe Ratio (daily/step estimation)
        returns = []
        for i in range(1, len(self.equity_curve)):
            ret = (self.equity_curve[i] - self.equity_curve[i - 1]) / self.equity_curve[i - 1]
            returns.append(ret)

        sharpe = 0.0
        if len(returns) > 2:
            mean_ret = sum(returns) / len(returns)
            std_ret = math.sqrt(sum((r - mean_ret) ** 2 for r in returns) / len(returns))
            if std_ret > 0:
                sharpe = round((mean_ret / std_ret) * math.sqrt(250), 2)

        return BacktestResult(
            trades=self.trades,
            equity_curve=self.equity_curve,
            total_return_pct=total_return_pct,
            sharpe_ratio=sharpe,
            max_drawdown_pct=round(max_dd * 100.0, 2),
            win_rate=win_rate,
            total_fees_paid=round(total_fees, 2),
            total_trades=len(self.trades),
        )
