"""Database engine and session management"""

import os
from typing import Generator
from sqlalchemy import create_engine, event, Engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from .models import Base

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database/jobs.db")

# Ensure database directory exists
if DATABASE_URL.startswith("sqlite:///"):
    db_path = DATABASE_URL.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Create engine with appropriate settings for SQLite
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=os.getenv("DEBUG", "false").lower() == "true"
    )
    
    # Enable foreign keys for SQLite
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # For PostgreSQL or other databases
    engine = create_engine(
        DATABASE_URL,
        echo=os.getenv("DEBUG", "false").lower() == "true"
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db() -> None:
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized successfully")


def drop_db() -> None:
    """Drop all tables - WARNING: Destructive operation"""
    if input("⚠️  WARNING: This will delete all tables. Type 'yes' to confirm: ") == "yes":
        Base.metadata.drop_all(bind=engine)
        print("✓ Database dropped")
    else:
        print("✗ Operation cancelled")


def get_db() -> Generator[Session, None, None]:
    """Dependency injection for database sessions"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DatabaseManager:
    """Database connection and transaction management"""

    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal

    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()

    def create_all_tables(self) -> None:
        """Create all tables in database"""
        Base.metadata.create_all(bind=self.engine)

    def drop_all_tables(self) -> None:
        """Drop all tables in database"""
        Base.metadata.drop_all(bind=self.engine)

    def health_check(self) -> bool:
        """Check if database is accessible"""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"✗ Database health check failed: {str(e)}")
            return False

    def get_stats(self) -> dict:
        """Get database statistics"""
        from .models import Job, Application, ApplicationLog
        
        db = self.get_session()
        try:
            stats = {
                "total_jobs": db.query(Job).count(),
                "total_applications": db.query(Application).count(),
                "completed_applications": db.query(Application).filter(
                    Application.status == "completed"
                ).count(),
                "failed_applications": db.query(Application).filter(
                    Application.status == "failed"
                ).count(),
                "pending_applications": db.query(Application).filter(
                    Application.status.in_(["queued", "applying"])
                ).count(),
                "total_logs": db.query(ApplicationLog).count(),
            }
            return stats
        finally:
            db.close()


# Global instance
db_manager = DatabaseManager()
