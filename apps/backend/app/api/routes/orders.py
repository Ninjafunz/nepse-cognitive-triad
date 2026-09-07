"""Order execution and history API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.api.deps import get_db
from app.models.orders import Order
from app.schemas.orders import OrderCreateRequest, OrderResponse
from app.services.trading.paper_trader import paper_trader
from app.services.settlement.ledger_service import ledger_service

router = APIRouter()


@router.post("/", response_model=OrderResponse)
async def create_paper_order(
    order_in: OrderCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """Submits a virtual paper trade order adhering to NEPSE rules and T+2 balances."""
    await ledger_service.initialize_account_balance(db)
    order = await paper_trader.execute_order(
        session=db,
        symbol=order_in.symbol.upper(),
        side=order_in.side,
        quantity=order_in.quantity,
        order_type=order_in.order_type,
        limit_price=order_in.limit_price,
    )
    if order.status == "REJECTED":
        raise HTTPException(status_code=400, detail=order.rejection_reason)
    return order


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Retrieves order history."""
    stmt = select(Order).order_by(desc(Order.created_at)).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()
