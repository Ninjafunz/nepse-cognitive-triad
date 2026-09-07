"""High fidelity simulated order matching engine."""

from typing import Tuple, Optional
from app.services.trading.slippage import fee_calculator


class OrderSimulator:
    """Matches simulated orders against current market prices and order books."""

    def evaluate_fill(
        self,
        side: str,
        order_type: str,
        quantity: int,
        limit_price: Optional[float],
        ltp: float,
        avg_volume: float = 20000.0,
    ) -> Tuple[bool, float, str]:
        """Returns (is_filled, avg_fill_price, rejection_or_fill_status)."""
        slippage_pct = fee_calculator.estimate_slippage_pct(quantity, avg_volume)
        simulated_price = fee_calculator.simulate_execution_price(ltp, side, slippage_pct)

        if order_type.upper() == "MARKET":
            return True, simulated_price, "FILLED"

        if order_type.upper() == "LIMIT":
            if limit_price is None:
                return False, 0.0, "REJECTED: Limit price required for LIMIT order"

            if side.upper() == "BUY":
                if simulated_price <= limit_price:
                    return True, simulated_price, "FILLED"
                else:
                    return False, 0.0, "PENDING: Limit price below market ask"
            else:  # SELL
                if simulated_price >= limit_price:
                    return True, simulated_price, "FILLED"
                else:
                    return False, 0.0, "PENDING: Limit price above market bid"

        return False, 0.0, f"REJECTED: Unsupported order type {order_type}"


order_simulator = OrderSimulator()
