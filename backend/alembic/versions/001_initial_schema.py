"""initial_schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-10-21 11:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. problems table
    op.create_table(
        'problems',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=False, server_default='leetcode'),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=200), nullable=False),
        sa.Column('title', sa.String(length=300), nullable=False),
        sa.Column('difficulty', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False, server_default=''),
        sa.Column('constraints', sa.JSON(), nullable=False),
        sa.Column('input_schema', sa.JSON(), nullable=False),
        sa.Column('support_status', sa.String(length=30), nullable=False, server_default='SUPPORTED'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_problems_source_id'), 'problems', ['source_id'], unique=False)
    op.create_index(op.f('ix_problems_slug'), 'problems', ['slug'], unique=True)

    # 2. test_cases table
    op.create_table(
        'test_cases',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('problem_id', sa.Uuid(), nullable=False),
        sa.Column('raw_input', sa.Text(), nullable=False),
        sa.Column('structured_input', sa.JSON(), nullable=False),
        sa.Column('category', sa.String(length=30), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=False),
        sa.Column('generation_method', sa.String(length=40), nullable=False, server_default='DETERMINISTIC_STRATEGY'),
        sa.Column('provenance', sa.String(length=200), nullable=False, server_default='generator'),
        sa.Column('validation_status', sa.String(length=30), nullable=False, server_default='VALIDATED'),
        sa.Column('fingerprint', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_cases_problem_id'), 'test_cases', ['problem_id'], unique=False)
    op.create_index(op.f('ix_test_cases_fingerprint'), 'test_cases', ['fingerprint'], unique=False)

    # 3. oracle_results table
    op.create_table(
        'oracle_results',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('test_case_id', sa.Uuid(), nullable=False),
        sa.Column('expected_output', sa.Text(), nullable=True),
        sa.Column('comparison_mode', sa.String(length=30), nullable=False, server_default='EXACT_MATCH'),
        sa.Column('oracle_source', sa.String(length=100), nullable=False, server_default='unverified'),
        sa.Column('verification_status', sa.String(length=30), nullable=False, server_default='UNVERIFIED'),
        sa.ForeignKeyConstraint(['test_case_id'], ['test_cases.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('test_case_id')
    )

    # 4. generation_runs table
    op.create_table(
        'generation_runs',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('problem_id', sa.Uuid(), nullable=False),
        sa.Column('requested_count', sa.Integer(), nullable=False),
        sa.Column('requested_categories', sa.JSON(), nullable=False),
        sa.Column('seed', sa.Integer(), nullable=False),
        sa.Column('generated_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('deduplicated_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('duration_ms', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='SUCCESS'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_generation_runs_problem_id'), 'generation_runs', ['problem_id'], unique=False)

    # 5. sync_runs table
    op.create_table(
        'sync_runs',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=False, server_default='huggingface'),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('inserted_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('updated_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='SUCCESS'),
        sa.Column('error_summary', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('sync_runs')
    op.drop_index(op.f('ix_generation_runs_problem_id'), table_name='generation_runs')
    op.drop_table('generation_runs')
    op.drop_table('oracle_results')
    op.drop_index(op.f('ix_test_cases_fingerprint'), table_name='test_cases')
    op.drop_index(op.f('ix_test_cases_problem_id'), table_name='test_cases')
    op.drop_table('test_cases')
    op.drop_index(op.f('ix_problems_slug'), table_name='problems')
    op.drop_index(op.f('ix_problems_source_id'), table_name='problems')
    op.drop_table('problems')
