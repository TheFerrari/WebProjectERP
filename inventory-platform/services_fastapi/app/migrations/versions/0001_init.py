"""init

Revision ID: 0001
Revises:
Create Date: 2026-01-01
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('services_branches',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=128), nullable=False, unique=True),
        sa.Column('location', sa.String(length=255), nullable=False),
        sa.Column('timezone', sa.String(length=64), nullable=False),
    )
    op.create_table('services_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('sku', sa.String(length=64), nullable=False, unique=True),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.Column('description', sa.String(length=500), nullable=False),
        sa.Column('unit', sa.String(length=16), nullable=False),
        sa.Column('min_stock_level', sa.Integer(), nullable=False),
    )
    op.create_table('services_stock',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('branch_id', sa.Integer(), sa.ForeignKey('services_branches.id')),
        sa.Column('item_id', sa.Integer(), sa.ForeignKey('services_items.id')),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.UniqueConstraint('branch_id', 'item_id')
    )
    op.create_table('services_orders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('branch_id', sa.Integer(), sa.ForeignKey('services_branches.id')),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    op.create_table('services_order_lines',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('order_id', sa.Integer(), sa.ForeignKey('services_orders.id')),
        sa.Column('item_id', sa.Integer(), sa.ForeignKey('services_items.id')),
        sa.Column('requested_qty', sa.Integer(), nullable=False),
        sa.Column('fulfilled_qty', sa.Integer(), nullable=False),
    )
    op.create_table('services_audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('actor_user_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(length=120), nullable=False),
        sa.Column('entity_type', sa.String(length=120), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('ip', sa.String(length=64), nullable=False),
        sa.Column('details', sa.JSON(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('services_audit_logs')
    op.drop_table('services_order_lines')
    op.drop_table('services_orders')
    op.drop_table('services_stock')
    op.drop_table('services_items')
    op.drop_table('services_branches')
