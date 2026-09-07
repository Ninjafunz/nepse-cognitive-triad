"""Paper Trading Execution Engine enforcing NEPSE circuit breakers and T+2 balances."""

from datetime import date
from typing import Dict, Any, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.orders import Order
from app.models.positions import Position
from app.models.securities import Security
from app.models.ledger import AccountLedger
from app.services.trading.slippage import fee_calculator
from app.services.trading.order_simulator import order_simulator
from app.services.settlement.t2_engine import t2_engine
from app.services.settlement.ledger_service import ledger_service
from app.config import settings


class PaperTradingEngine:
    """Executes virtual orders, validates trading constraints, and adjusts T+2 ledgers."""

    async def execute_order(
        self,
        session: AsyncSession,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str = "MARKET",
        limit_price: float = None,
        ai_confidence: float = None,
    ) -> Order:
        today = date.today()
        settled_date = t2_engine.calculate_settlement_date(today)

        # 1. Fetch Security & Base Reference Price
        sec_stmt = select(Security).where(Security.symbol == symbol)
        security = (await session.execute(sec_stmt)).scalar_one_or_none()
        if not security:
            order = Order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                status="REJECTED",
                rejection_reason=f"Security {symbol} not found in database",
            )
            session.add(order)
            await session.commit()
            return order

        base_price = security.base_price or 500.0
        ltp = base_price

        # 2. Check NEPSE Circuit Breakers (±10% from base price)
        lower_band = base_price * (1.0 - settings.CIRCUIT_BREAKER_NORMAL_PCT)
        upper_band = base_price * (1.0 + settings.CIRCUIT_BREAKER_NORMAL_PCT)

        if limit_price:
            if limit_price < lower_band or limit_price > upper_band:
                order = Order(
                    symbol=symbol,
                    side=side,
                    order_type=order_type,
                    quantity=quantity,
                    limit_price=limit_price,
                    status="REJECTED",
                    rejection_reason=f"Circuit Breaker Violated: Price {limit_price} outside [{lower_band:.1f}, {upper_band:.1f}]",
                )
                session.add(order)
                await session.commit()
                return order

        # 3. Position check for SELL (Strictly No Short Selling)
        pos_stmt = select(Position).where(Position.symbol == symbol)
        position = (await session.execute(pos_stmt)).scalar_one_or_none()

        if side.upper() == "SELL":
            current_qty = position.quantity if position else 0
            if current_qty < quantity:
                order = Order(
                    symbol=symbol,
                    side=side,
                    order_type=order_type,
                    quantity=quantity,
                    status="REJECTED",
                    rejection_reason=f"No Short Selling: Owned {current_qty} shares, attempted to sell {quantity}",
                )
                session.add(order)
                await session.commit()
                return order

        # 4. Fill Simulation with Slippage
        is_filled, fill_price, status_msg = order_simulator.evaluate_fill(
            side=side,
            order_type=order_type,
            quantity=quantity,
            limit_price=limit_price,
            ltp=ltp,
        )

        if not is_filled:
            order = Order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                limit_price=limit_price,
                status="PENDING" if "PENDING" in status_msg else "REJECTED",
                rejection_reason=status_msg,
            )
            session.add(order)
            await session.commit()
            return order

        # 5. Calculate Costs & Check Buying Power
        trade_value = round(fill_price * quantity, 2)
        fees = fee_calculator.calculate_fees(trade_value, side)
        total_debit_or_credit = trade_value + fees["total_fees"] if side.upper() == "BUY" else trade_value - fees["total_fees"]

        if side.upper() == "BUY":
            portfolio_summary = await ledger_service.get_portfolio_summary(session)
            available_power = portfolio_summary["available_buying_power_npr"]
            if available_power < total_debit_or_credit:
                order = Order(
                    symbol=symbol,
                    side=side,
                    order_type=order_type,
                    quantity=quantity,
                    status="REJECTED",
                    rejection_reason=f"Insufficient settled funds: Needed NPR {total_debit_or_credit:,.2f}, Available: NPR {available_power:,.2f}",
                )
                session.add(order)
                await session.commit()
                return order

        # 6. Record Filled Order
        order = Order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            limit_price=limit_price,
            filled_qty=quantity,
            avg_fill_price=fill_price,
            broker_commission=fees["broker_commission"],
            sebon_fee=fees["sebon_fee"],
            dp_charge=fees["dp_charge"],
            total_cost=total_debit_or_credit,
            status="FILLED",
            ai_confidence=ai_confidence,
        )
        session.add(order)
        await session.flush()

        # 7. Update Ledger
        ledger_amount = -total_debit_or_credit if side.upper() == "BUY" else total_debit_or_credit
        ledger_entry = AccountLedger(
            entry_type="buy" if side.upper() == "BUY" else "sell",
            amount=ledger_amount,
            currency="NPR",
            trade_date=today,
            settled_date=settled_date,
            order_id=order.id,
            description=f"Executed {side} {quantity} {symbol} @ NPR {fill_price} (Settles on {settled_date})",
        )
        session.add(ledger_entry)

        # 8. Update Position
        if not position:
            position = Position(symbol=symbol, quantity=0, avg_cost=0.0, current_price=fill_price)
            session.add(position)

        if side.upper() == "BUY":
            new_qty = position.quantity + quantity
            new_total_cost = (position.quantity * position.avg_cost) + (quantity * fill_price)
            position.avg_cost = round(new_total_cost / new_qty, 2)
            position.quantity = new_qty
            position.current_price = fill_price
            position.unrealized_pnl = round((fill_price - position.avg_cost) * position.quantity, 2)
        else:  # SELL
            realized_pnl_chunk = (fill_price - position.avg_cost) * quantity - fees["total_fees"]
            position.realized_pnl += round(realized_pnl_chunk, 2)
            position.quantity -= quantity
            position.current_price = fill_price
            position.unrealized_pnl = round((fill_price - position.avg_cost) * position.quantity, 2)

        await session.commit()
        return order


paper_trader = PaperTradingEngine()
