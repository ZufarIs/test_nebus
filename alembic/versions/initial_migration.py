"""initial migration

Revision ID: initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Activities
    op.create_table(
        'activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('level', sa.Integer(), nullable=False, default=1),
        sa.ForeignKeyConstraint(['parent_id'], ['activities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_activities_id', 'activities', ['id'])
    op.create_index('ix_activities_name', 'activities', ['name'])

    # Buildings
    op.create_table(
        'buildings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_buildings_id', 'buildings', ['id'])
    op.create_index('ix_buildings_address', 'buildings', ['address'])

    # Organizations
    op.create_table(
        'organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('building_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['building_id'], ['buildings.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_organizations_id', 'organizations', ['id'])
    op.create_index('ix_organizations_name', 'organizations', ['name'])

    # Organization phones
    op.create_table(
        'organization_phones',
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('organization_id', 'phone')
    )

    # Organization activities
    op.create_table(
        'organization_activities',
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('activity_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('organization_id', 'activity_id')
    )

def downgrade() -> None:
    op.drop_table('organization_activities')
    op.drop_table('organization_phones')
    op.drop_table('organizations')
    op.drop_table('buildings')
    op.drop_table('activities') 
