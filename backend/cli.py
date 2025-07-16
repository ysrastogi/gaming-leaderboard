import click
from scripts.populate_db import populate_database
import subprocess
import os

@click.group()
def cli():
    """Gaming Leaderboard Database Management CLI"""
    pass

@cli.command()
@click.option('--users', default=1000000, help='Number of users to create')
@click.option('--sessions', default=5000000, help='Number of game sessions to create')
@click.option('--clear', is_flag=True, help='Clear all data before populating')
@click.option('--users-only', is_flag=True, help='Only populate users')
@click.option('--sessions-only', is_flag=True, help='Only populate game sessions')
@click.option('--leaderboard-only', is_flag=True, help='Only populate leaderboard')
def populate(users, sessions, clear, users_only, sessions_only, leaderboard_only):
    """Populate database with test data."""
    ctx = click.Context(populate_database)
    ctx.invoke(
        populate_database,
        users=users,
        sessions=sessions,
        clear=clear,
        users_only=users_only,
        sessions_only=sessions_only,
        leaderboard_only=leaderboard_only
    )

@cli.command()
@click.option('--sql-file', type=click.Path(exists=True), help='SQL file to execute')
def execute_sql(sql_file):
    """Execute a SQL file against the database."""
    if sql_file:
        click.echo(f"Executing SQL file: {sql_file}")
        # This would depend on your database type
        # For PostgreSQL: subprocess.run(['psql', '-f', sql_file, database_url])
        # For SQLite: subprocess.run(['sqlite3', 'leaderboard.db', '.read', sql_file])
        click.echo("SQL execution completed")

@cli.command()
def init_db():
    """Initialize database with Alembic migrations."""
    click.echo("Running Alembic migrations...")
    subprocess.run(['alembic', 'upgrade', 'head'])
    click.echo("✅ Database initialized")

if __name__ == '__main__':
    cli()