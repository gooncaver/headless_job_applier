"""Main entry point for Headless Job Applier"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import click
from database.engine import db_manager
from utils.logging_config import logger
from utils.credentials import CredentialManager


@click.group()
def cli():
    """Headless Job Applier - Automated job scraping and application"""
    pass


@cli.command()
def setup():
    """Initialize application (first-time setup)"""
    logger.info("🚀 Initializing Headless Job Applier...")
    
    # Step 1: Create database
    logger.info("Step 1/3: Creating database...")
    db_manager.create_all_tables()
    
    # Step 2: Generate encryption key if not exists
    logger.info("Step 2/3: Setting up credential encryption...")
    if not os.getenv("ENCRYPTION_KEY"):
        key = CredentialManager.generate_key()
        logger.warning(f"No ENCRYPTION_KEY found. Add this to your .env file:")
        logger.warning(f"ENCRYPTION_KEY={key}")
    else:
        logger.info("✓ ENCRYPTION_KEY already configured")
    
    # Step 3: Verify database
    logger.info("Step 3/3: Verifying database...")
    if db_manager.health_check():
        logger.info("✓ Database is operational")
        stats = db_manager.get_stats()
        logger.info(f"  - Jobs: {stats['total_jobs']}")
        logger.info(f"  - Applications: {stats['total_applications']}")
    else:
        logger.error("✗ Database health check failed")
        sys.exit(1)
    
    logger.info("✅ Setup complete!")
    logger.info("Next steps:")
    logger.info("  1. Configure your credentials in .env file")
    logger.info("  2. Fill in input/user_profile.yaml with your information")
    logger.info("  3. Run: python src/main.py scrape")


@cli.command()
def status():
    """Show application status and statistics"""
    logger.info("📊 Headless Job Applier Status")
    logger.info("=" * 50)
    
    if not db_manager.health_check():
        logger.error("✗ Database not accessible")
        sys.exit(1)
    
    stats = db_manager.get_stats()
    logger.info(f"Total Jobs Scraped: {stats['total_jobs']}")
    logger.info(f"Total Applications: {stats['total_applications']}")
    logger.info(f"  ├─ Completed: {stats['completed_applications']}")
    logger.info(f"  ├─ Failed: {stats['failed_applications']}")
    logger.info(f"  └─ Pending: {stats['pending_applications']}")
    logger.info(f"Total Logs: {stats['total_logs']}")


@cli.command()
def scrape():
    """Run job scraper (not implemented in Phase 1)"""
    logger.info("🔍 Job Scraper")
    logger.info("(Phase 1 implementation - to be completed in Week 2)")
    logger.warning("Scraper implementation coming soon...")
    logger.info("For now, you can test the database setup.")


@cli.command()
def customize():
    """Customize resumes (not implemented in Phase 1)"""
    logger.info("📝 Resume Customizer")
    logger.info("(Phase 2 implementation - to be completed in Week 4)")
    logger.warning("Customizer implementation coming soon...")


@cli.command()
def apply():
    """Apply to selected jobs (not implemented in Phase 1)"""
    logger.info("🚀 Job Application Filler")
    logger.info("(Phase 3 implementation - to be completed in Week 6)")
    logger.warning("Applier implementation coming soon...")


@cli.command()
def init_db_cmd():
    """Initialize database (create tables)"""
    logger.info("Creating database tables...")
    db_manager.create_all_tables()
    logger.info("✓ Database initialized")


@cli.command()
def generate_key():
    """Generate encryption key for credentials"""
    key = CredentialManager.generate_key()
    logger.info("Generated encryption key:")
    logger.info(key)
    logger.info("\nAdd this to your .env file:")
    logger.info(f"ENCRYPTION_KEY={key}")


@cli.command()
def test_db():
    """Test database connectivity"""
    logger.info("🧪 Testing Database Connection...")
    if db_manager.health_check():
        logger.info("✓ Database connection successful")
        stats = db_manager.get_stats()
        logger.info(f"✓ Database stats: {stats}")
    else:
        logger.error("✗ Database health check failed")
        sys.exit(1)


@cli.command()
@click.option("--dry-run", is_flag=True, help="Show what would be done without making changes")
def reset_db(dry_run):
    """Reset database (WARNING: Destructive)"""
    if dry_run:
        logger.info("🧪 DRY RUN: Would reset database")
        logger.warning("Run without --dry-run to confirm")
    else:
        logger.warning("⚠️  This will delete all jobs and applications!")
        confirm = input("Type 'yes' to confirm: ")
        if confirm == "yes":
            db_manager.drop_all_tables()
            db_manager.create_all_tables()
            logger.info("✓ Database reset complete")
        else:
            logger.info("✗ Operation cancelled")


def main():
    """Main entry point"""
    try:
        cli()
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
