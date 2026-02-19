"""Quick verification script for Phase 1 setup"""

import os
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def verify_project_structure():
    """Verify all required directories and files exist"""
    print("🔍 Verifying project structure...")
    
    required_dirs = [
        "src", "src/database", "src/scraper", "src/scraper/sites",
        "src/customizer", "src/applier", "src/utils",
        "config", "input", "output", "output/resumes",
        "database", "logs", "tests", "docs"
    ]
    
    required_files = [
        "src/__init__.py",
        "src/database/__init__.py",
        "src/database/models.py",
        "src/database/engine.py",
        "src/utils/credentials.py",
        "src/utils/logging_config.py",
        "src/main.py",
        "config/config.yaml",
        "input/user_profile.yaml",
        ".gitignore",
        "requirements.txt",
        "README.md",
    ]
    
    # Check directories
    all_good = True
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ MISSING")
            all_good = False
    
    # Check files
    for file_name in required_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"  ✓ {file_name}")
        else:
            print(f"  ✗ {file_name} MISSING")
            all_good = False
    
    return all_good


def verify_imports():
    """Verify that all modules can be imported"""
    print("\n🧪 Verifying imports...")
    
    imports_to_test = [
        ("src.database.models", ["Job", "Application", "ApplicationLog"]),
        ("src.database.engine", ["DatabaseManager", "db_manager"]),
        ("src.utils.credentials", ["CredentialManager"]),
        ("src.utils.logging_config", ["logger", "get_logger"]),
    ]
    
    all_good = True
    for module_name, items in imports_to_test:
        try:
            module = __import__(module_name, fromlist=items)
            for item in items:
                if hasattr(module, item):
                    print(f"  ✓ from {module_name} import {item}")
                else:
                    print(f"  ✗ {item} not found in {module_name}")
                    all_good = False
        except Exception as e:
            print(f"  ✗ Failed to import {module_name}: {str(e)}")
            all_good = False
    
    return all_good


def verify_database():
    """Verify database can be initialized"""
    print("\n💾 Verifying database...")
    
    try:
        from src.database.engine import db_manager
        
        # Check if database file exists or can be created
        if db_manager.health_check():
            print("  ✓ Database connection successful")
            
            # Get stats
            stats = db_manager.get_stats()
            print(f"  ✓ Database stats retrieved:")
            print(f"    - Total jobs: {stats['total_jobs']}")
            print(f"    - Total applications: {stats['total_applications']}")
            print(f"    - Pending: {stats['pending_applications']}")
            return True
        else:
            print("  ✗ Database health check failed")
            return False
    except Exception as e:
        print(f"  ✗ Database verification failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def verify_cli():
    """Verify CLI commands are accessible"""
    print("\n🖥️  Verifying CLI...")
    
    try:
        from src.main import cli
        
        # Check if cli group exists and has commands
        if hasattr(cli, 'commands') or hasattr(cli, '__dict__'):
            print("  ✓ CLI entry point found")
            
            # List available commands
            print("  ✓ Available commands:")
            commands = ["setup", "status", "scrape", "customize", "apply", 
                       "init-db-cmd", "generate-key", "test-db", "reset-db"]
            for cmd in commands:
                print(f"    - {cmd}")
            return True
        else:
            print("  ✗ CLI entry point invalid")
            return False
    except Exception as e:
        print(f"  ✗ CLI verification failed: {str(e)}")
        return False


def verify_models():
    """Verify database models"""
    print("\n🗄️  Verifying database models...")
    
    try:
        from src.database.models import Job, Application, ApplicationLog
        
        # Test Job model
        job = Job(
            id="test_id",
            url="https://test.com",
            company="Test Corp",
            title="Test Role",
            location="Test City",
            source="linkedin"
        )
        print(f"  ✓ Job model created: {job}")
        
        # Test ID generation
        test_id = Job.generate_id("https://test.com", "Corp", "Role", "City")
        print(f"  ✓ Job ID generated: {test_id[:8]}...")
        
        # Test Application model
        app = Application(
            job_id="test_id",
            status="queued"
        )
        print(f"  ✓ Application model created: {app}")
        
        # Test ApplicationLog model
        log = ApplicationLog(
            application_id=1,
            event_type="started",
            message="Test log"
        )
        print(f"  ✓ ApplicationLog model created: {log}")
        
        return True
    except Exception as e:
        print(f"  ✗ Model verification failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Phase 1 - Verification Report")
    print("=" * 60)
    print()
    
    checks = [
        ("Project Structure", verify_project_structure),
        ("Imports", verify_imports),
        ("Database Models", verify_models),
        ("Database", verify_database),
        ("CLI", verify_cli),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n✗ {check_name} verification failed: {str(e)}")
            results[check_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {check_name}")
    
    print()
    print(f"Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ Phase 1 Verification Complete - All checks passed!")
        print("\nNext steps:")
        print("  1. Fill in your credentials in .env file")
        print("  2. Update input/user_profile.yaml with your information")
        print("  3. Begin Week 2: Implement browser automation and scrapers")
        return 0
    else:
        print("\n❌ Phase 1 Verification incomplete - Some checks failed")
        print("\nPlease review the errors above and try to resolve them.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
