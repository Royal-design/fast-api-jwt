"""create users/products and add image fields

Revision ID: 20260701_0001
Revises:
Create Date: 2026-07-01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260701_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return inspector.has_table(table_name)


def column_exists(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return any(column["name"] == column_name for column in inspector.get_columns(table_name))


def upgrade() -> None:
    if not table_exists("users"):
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("first_name", sa.String(length=50), nullable=False),
            sa.Column("last_name", sa.String(length=50), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("password", sa.String(length=255), nullable=False),
            sa.Column("image_url", sa.String(length=500), nullable=True),
            sa.Column("image_public_id", sa.String(length=255), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"),
        )
    else:
        if not column_exists("users", "image_url"):
            op.add_column("users", sa.Column("image_url", sa.String(length=500), nullable=True))
        if not column_exists("users", "image_public_id"):
            op.add_column(
                "users",
                sa.Column("image_public_id", sa.String(length=255), nullable=True),
            )

    if not table_exists("products"):
        op.create_table(
            "products",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("name", sa.String(length=100), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("price", sa.Float(), nullable=False),
            sa.Column("quantity", sa.Integer(), nullable=False),
            sa.Column("image_url", sa.String(length=500), nullable=True),
            sa.Column("image_public_id", sa.String(length=255), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
    else:
        if not column_exists("products", "image_url"):
            op.add_column("products", sa.Column("image_url", sa.String(length=500), nullable=True))
        if not column_exists("products", "image_public_id"):
            op.add_column(
                "products",
                sa.Column("image_public_id", sa.String(length=255), nullable=True),
            )


def downgrade() -> None:
    if table_exists("products"):
        if column_exists("products", "image_public_id"):
            op.drop_column("products", "image_public_id")
        if column_exists("products", "image_url"):
            op.drop_column("products", "image_url")

    if table_exists("users"):
        if column_exists("users", "image_public_id"):
            op.drop_column("users", "image_public_id")
        if column_exists("users", "image_url"):
            op.drop_column("users", "image_url")
