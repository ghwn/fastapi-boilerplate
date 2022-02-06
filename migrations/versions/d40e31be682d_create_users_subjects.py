"""create users subjects

Revision ID: d40e31be682d
Revises: 711a7256a242
Create Date: 2022-02-06 15:55:17.789866

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d40e31be682d"
down_revision = "711a7256a242"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "subjects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_subjects_id"), "subjects", ["id"], unique=False)
    op.create_index(op.f("ix_subjects_name"), "subjects", ["name"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_subjects_name"), table_name="subjects")
    op.drop_index(op.f("ix_subjects_id"), table_name="subjects")
    op.drop_table("subjects")
