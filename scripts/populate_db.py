import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from app.core.database import engine, SessionLocal
from app.models import User, GameSession, Leaderboard
import click
import time

def populate_users(db: Session, count: int = 1000000):
    """Populate users table with bulk insert for better performance."""
    click.echo(f"Populating {count} users...")
    
    # For SQLite, we'll use a different approach since it doesn't have generate_series
    if 'sqlite' in str(engine.url):
        # Batch insert users for SQLite
        batch_size = 10000
        for i in range(0, count, batch_size):
            users_batch = []
            for j in range(i, min(i + batch_size, count)):
                users_batch.append({
                    'username': f'user_{j+1}',
                    'join_date': datetime.utcnow()  # Add join_date
                })
            
            if users_batch:
                db.execute(
                    text("INSERT INTO users (username, join_date) VALUES (:username, :join_date)"),
                    users_batch
                )
                db.commit()
                
            if (i + batch_size) % 100000 == 0:
                click.echo(f"Inserted {i + batch_size} users...")
    else:
        # For PostgreSQL with generate_series
        db.execute(
            text("""
                INSERT INTO users (username, join_date)
                SELECT 'user_' || generate_series(1, :count), NOW()
            """),
            {"count": count}
        )
        db.commit()
    
    click.echo(f"✅ Successfully populated {count} users")

def populate_game_sessions(db: Session, count: int = 5000000):
    """Populate game sessions with random data."""
    click.echo(f"Populating {count} game sessions...")
    
    # Get user count
    user_count = db.query(func.count(User.id)).scalar()
    if user_count == 0:
        click.echo("❌ No users found. Please populate users first.")
        return
    
    batch_size = 10000
    game_modes = ['solo', 'team']
    
    for i in range(0, count, batch_size):
        sessions_batch = []
        for j in range(min(batch_size, count - i)):
            # Random data generation
            user_id = random.randint(1, user_count)
            score = random.randint(1, 10000)
            game_mode = random.choice(game_modes)
            # Random timestamp within last year
            timestamp = datetime.now() - timedelta(days=random.randint(0, 365))
            
            sessions_batch.append({
                'user_id': user_id,
                'score': score,
                'game_mode': game_mode,
                'timestamp': timestamp
            })
        
        if sessions_batch:
            db.execute(
                text("""
                    INSERT INTO game_sessions (user_id, score, game_mode, timestamp) 
                    VALUES (:user_id, :score, :game_mode, :timestamp)
                """),
                sessions_batch
            )
            db.commit()
            
        if (i + batch_size) % 100000 == 0:
            click.echo(f"Inserted {i + batch_size} game sessions...")
    
    click.echo(f"✅ Successfully populated {count} game sessions")

def populate_leaderboard(db: Session):
    """Populate leaderboard by aggregating scores."""
    click.echo("Populating leaderboard...")
    
    # Clear existing leaderboard
    db.execute(text("DELETE FROM leaderboard"))
    
    # SQLite compatible query for leaderboard aggregation
    if 'sqlite' in str(engine.url):
        db.execute(text("""
            INSERT INTO leaderboard (user_id, total_score, rank)
            SELECT 
                user_id, 
                AVG(score) as total_score,
                RANK() OVER (ORDER BY SUM(score) DESC) as rank
            FROM game_sessions 
            GROUP BY user_id
        """))
    else:
        # PostgreSQL version
        db.execute(text("""
            INSERT INTO leaderboard (user_id, total_score, rank)
            SELECT 
                user_id, 
                AVG(score) as total_score,
                RANK() OVER (ORDER BY SUM(score) DESC) as rank
            FROM game_sessions 
            GROUP BY user_id
        """))
    
    db.commit()
    click.echo("✅ Successfully populated leaderboard")

def clear_all_data(db: Session):
    """Clear all data from tables."""
    click.echo("Clearing all data...")
    db.execute(text("DELETE FROM leaderboard"))
    db.execute(text("DELETE FROM game_sessions"))
    db.execute(text("DELETE FROM users"))
    db.commit()
    click.echo("✅ All data cleared")

@click.command()
@click.option('--users', default=1000000, help='Number of users to create')
@click.option('--sessions', default=5000000, help='Number of game sessions to create')
@click.option('--clear', is_flag=True, help='Clear all data before populating')
@click.option('--users-only', is_flag=True, help='Only populate users')
@click.option('--sessions-only', is_flag=True, help='Only populate game sessions')
@click.option('--leaderboard-only', is_flag=True, help='Only populate leaderboard')
def populate_database(users, sessions, clear, users_only, sessions_only, leaderboard_only):
    """Populate the gaming leaderboard database with test data."""
    
    db = SessionLocal()
    start_time = time.time()
    
    try:
        if clear:
            clear_all_data(db)
        
        if users_only:
            populate_users(db, users)
        elif sessions_only:
            populate_game_sessions(db, sessions)
        elif leaderboard_only:
            populate_leaderboard(db)
        else:
            # Full population
            populate_users(db, users)
            populate_game_sessions(db, sessions)
            populate_leaderboard(db)
        
        end_time = time.time()
        click.echo(f"🎉 Database population completed in {end_time - start_time:.2f} seconds")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()