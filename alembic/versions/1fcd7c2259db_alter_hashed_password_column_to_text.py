"""Alter hashed_password column to Text

Revision ID: 1fcd7c2259db
Revises: 1100b70d461e
Create Date: 2024-11-26 06:28:26.408037

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fcd7c2259db'
down_revision: Union[str, None] = '1100b70d461e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alter hashed_password column to Text
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.VARCHAR(),
                    type_=sa.Text(),
                    existing_nullable=False)

    # Alter is_active column to Boolean with explicit casting
    op.execute(
        """
        ALTER TABLE users 
        ALTER COLUMN is_active 
        TYPE BOOLEAN 
        USING CASE 
            WHEN is_active = 'True' THEN true
            WHEN is_active = 'False' THEN false
            ELSE NULL
        END
        """
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'is_active',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('users', 'hashed_password',
               existing_type=sa.Text(length=255),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    # ### end Alembic commands ###
