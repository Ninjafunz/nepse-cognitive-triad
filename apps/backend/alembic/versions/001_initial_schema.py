"""initial_schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-08 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Enable Extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    # 2. Securities
    op.create_table(
        'securities',
        sa.Column('symbol', sa.String(length=20), primary_key=True),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('sector', sa.String(length=100), nullable=False),
        sa.Column('instrument_type', sa.String(length=50), server_default='Equity'),
        sa.Column('base_price', sa.Float(), nullable=True),
        sa.Column('listing_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_securities_symbol', 'securities', ['symbol'])
    op.create_index('ix_securities_sector', 'securities', ['sector'])

    # 3. Market Data (TimescaleDB hypertable)
    op.create_table(
        'market_data_1min',
        sa.Column('symbol', sa.String(length=20), nullable=False),
        sa.Column('time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('open', sa.Float(), nullable=False),
        sa.Column('high', sa.Float(), nullable=False),
        sa.Column('low', sa.Float(), nullable=False),
        sa.Column('close', sa.Float(), nullable=False),
        sa.Column('volume', sa.Float(), server_default='0.0'),
        sa.Column('ltp', sa.Float(), nullable=False),
        sa.Column('trade_count', sa.Integer(), server_default='0'),
        sa.PrimaryKeyConstraint('symbol', 'time'),
    )
    op.execute("SELECT create_hypertable('market_data_1min', 'time', if_not_exists => TRUE);")

    # 4. Corporate Actions
    op.create_table(
        'corporate_actions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('symbol', sa.String(length=20), sa.ForeignKey('securities.symbol', ondelete='CASCADE'), nullable=False),
        sa.Column('action_type', sa.String(length=50), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('announcement_date', sa.Date(), nullable=True),
        sa.Column('book_close_date', sa.Date(), nullable=True),
        sa.Column('record_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # 5. Account Ledger (T+2 Aware)
    op.create_table(
        'account_ledger',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('entry_type', sa.String(length=50), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(length=10), server_default='NPR'),
        sa.Column('trade_date', sa.Date(), nullable=False),
        sa.Column('settled_date', sa.Date(), nullable=False),
        sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_account_ledger_settled_date', 'account_ledger', ['settled_date'])

    # 6. Orders
    op.create_table(
        'orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('symbol', sa.String(length=20), sa.ForeignKey('securities.symbol', ondelete='CASCADE'), nullable=False),
        sa.Column('side', sa.String(length=10), nullable=False),
        sa.Column('order_type', sa.String(length=20), server_default='MARKET'),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('limit_price', sa.Float(), nullable=True),
        sa.Column('filled_qty', sa.Integer(), server_default='0'),
        sa.Column('avg_fill_price', sa.Float(), server_default='0.0'),
        sa.Column('broker_commission', sa.Float(), server_default='0.0'),
        sa.Column('sebon_fee', sa.Float(), server_default='0.0'),
        sa.Column('dp_charge', sa.Float(), server_default='0.0'),
        sa.Column('total_cost', sa.Float(), server_default='0.0'),
        sa.Column('status', sa.String(length=30), server_default='PENDING'),
        sa.Column('rejection_reason', sa.String(length=255), nullable=True),
        sa.Column('ai_confidence', sa.Float(), nullable=True),
        sa.Column('triad_decision_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("side IN ('BUY', 'SELL')", name='check_valid_order_side_no_short'),
    )

    # 7. Positions
    op.create_table(
        'positions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('symbol', sa.String(length=20), sa.ForeignKey('securities.symbol', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column('quantity', sa.Integer(), server_default='0'),
        sa.Column('avg_cost', sa.Float(), server_default='0.0'),
        sa.Column('current_price', sa.Float(), server_default='0.0'),
        sa.Column('unrealized_pnl', sa.Float(), server_default='0.0'),
        sa.Column('realized_pnl', sa.Float(), server_default='0.0'),
        sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # 8. Triad Decisions
    op.create_table(
        'triad_decisions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('symbol', sa.String(length=20), sa.ForeignKey('securities.symbol', ondelete='CASCADE'), nullable=False),
        sa.Column('alpha_score', sa.Float(), nullable=False),
        sa.Column('alpha_rationale', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('beta_score', sa.Float(), nullable=False),
        sa.Column('beta_rationale', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('gamma_score', sa.Float(), nullable=False),
        sa.Column('gamma_rationale', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('final_score', sa.Float(), nullable=False),
        sa.Column('disagreement_std', sa.Float(), server_default='0.0'),
        sa.Column('gamma_vetoed', sa.Boolean(), server_default='false'),
        sa.Column('action_taken', sa.String(length=20), nullable=False),
        sa.Column('confidence_score', sa.Float(), server_default='0.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # 9. Trade Journals & Post Trade Reflections
    op.create_table(
        'trade_journals',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('triad_decision_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('triad_decisions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('journal_type', sa.String(length=30), server_default='pre_trade'),
        sa.Column('thesis_summary', sa.String(length=500), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('citations', postgresql.JSONB(astext_type=sa.Text()), server_default='[]'),
        sa.Column('model_used', sa.String(length=50), server_default='llama3:70b'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'post_trade_reflections',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('order_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('orders.id', ondelete='CASCADE'), nullable=False),
        sa.Column('original_thesis', sa.Text(), nullable=False),
        sa.Column('actual_outcome', sa.Text(), nullable=False),
        sa.Column('reflection_content', sa.Text(), nullable=False),
        sa.Column('route_accuracy', postgresql.JSONB(astext_type=sa.Text()), server_default='{}'),
        sa.Column('lesson_learned', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # 10. Literature Knowledge (pgvector)
    op.create_table(
        'literature_knowledge',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('author', sa.String(length=100), nullable=False),
        sa.Column('work_title', sa.String(length=255), nullable=False),
        sa.Column('route_affinity', sa.String(length=20), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('chunk_text', sa.Text(), nullable=False),
        sa.Column('embedding', Vector(1536), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('literature_knowledge')
    op.drop_table('post_trade_reflections')
    op.drop_table('trade_journals')
    op.drop_table('triad_decisions')
    op.drop_table('positions')
    op.drop_table('orders')
    op.drop_table('account_ledger')
    op.drop_table('corporate_actions')
    op.drop_table('market_data_1min')
    op.drop_table('securities')
