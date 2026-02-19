"""Unit tests for database models"""

import pytest
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Job, Application, ApplicationLog


@pytest.fixture
def db_engine():
    """Create in-memory SQLite database for testing"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    """Create a new database session for tests"""
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    yield session
    session.close()


class TestJobModel:
    """Test Job model"""

    def test_create_job(self, db_session):
        """Test creating a job record"""
        job = Job(
            id="abc123456789",
            url="https://example.com/job/123",
            company="Tech Corp",
            title="Data Engineer",
            location="San Francisco",
            description="Build data pipelines",
            source="linkedin"
        )
        db_session.add(job)
        db_session.commit()

        retrieved = db_session.query(Job).filter_by(id="abc123456789").first()
        assert retrieved is not None
        assert retrieved.company == "Tech Corp"
        assert retrieved.title == "Data Engineer"

    def test_job_id_generation(self):
        """Test job ID generation for deduplication"""
        job_id = Job.generate_id(
            url="https://linkedin.com/job/123",
            company="Palantir",
            title="Data Engineer",
            location="SF"
        )
        
        # Same inputs should produce same ID
        job_id_2 = Job.generate_id(
            url="https://linkedin.com/job/123",
            company="Palantir",
            title="Data Engineer",
            location="SF"
        )
        assert job_id == job_id_2

        # Different inputs should produce different IDs
        job_id_3 = Job.generate_id(
            url="https://indeed.com/job/456",
            company="Google",
            title="ML Engineer",
            location="NYC"
        )
        assert job_id != job_id_3

    def test_job_is_stale(self, db_session):
        """Test job staleness check"""
        old_job = Job(
            id="old_job",
            url="https://example.com/old",
            company="Old Corp",
            title="Old Role",
            location="SF",
            source="linkedin",
            scraped_at=datetime.utcnow() - timedelta(days=10)
        )
        
        new_job = Job(
            id="new_job",
            url="https://example.com/new",
            company="New Corp",
            title="New Role",
            location="SF",
            source="linkedin",
            scraped_at=datetime.utcnow()
        )
        
        db_session.add_all([old_job, new_job])
        db_session.commit()

        assert old_job.is_stale(days=7) is True
        assert new_job.is_stale(days=7) is False

    def test_unique_url_constraint(self, db_session):
        """Test that URLs must be unique"""
        job1 = Job(
            id="job1",
            url="https://duplicate.com",
            company="Company A",
            title="Role A",
            location="SF",
            source="linkedin"
        )
        
        job2 = Job(
            id="job2",
            url="https://duplicate.com",  # Same URL!
            company="Company B",
            title="Role B",
            location="NYC",
            source="indeed"
        )
        
        db_session.add(job1)
        db_session.commit()
        db_session.add(job2)
        
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()

    def test_job_representation(self):
        """Test job string representation"""
        job = Job(
            id="test_id",
            url="https://test.com",
            company="Test Corp",
            title="Test Role",
            location="Test City",
            source="linkedin"
        )
        
        repr_str = repr(job)
        assert "Test Corp" in repr_str
        assert "Test Role" in repr_str


class TestApplicationModel:
    """Test Application model"""

    def test_create_application(self, db_session):
        """Test creating an application record"""
        job = Job(
            id="job1",
            url="https://test.com/job",
            company="Test Corp",
            title="Data Engineer",
            location="SF",
            source="linkedin"
        )
        db_session.add(job)
        db_session.commit()

        app = Application(
            job_id="job1",
            status="queued"
        )
        db_session.add(app)
        db_session.commit()

        retrieved = db_session.query(Application).first()
        assert retrieved is not None
        assert retrieved.status == "queued"
        assert retrieved.job_id == "job1"

    def test_application_status_transitions(self, db_session):
        """Test application status changes"""
        job = Job(
            id="job1",
            url="https://test.com",
            company="Corp",
            title="Role",
            location="City",
            source="linkedin"
        )
        db_session.add(job)
        db_session.commit()

        app = Application(job_id="job1", status="queued")
        db_session.add(app)
        db_session.commit()

        # Simulate status transitions
        statuses = ["queued", "customizing", "ready", "applying", "completed"]
        for status in statuses:
            app.status = status
            db_session.commit()
            
            retrieved = db_session.query(Application).filter_by(id=app.id).first()
            assert retrieved.status == status

    def test_application_is_complete(self, db_session):
        """Test application completion check"""
        job = Job(
            id="job1",
            url="https://test.com",
            company="Corp",
            title="Role",
            location="City",
            source="linkedin"
        )
        db_session.add(job)
        db_session.commit()

        # Active application
        app_active = Application(job_id="job1", status="applying")
        db_session.add(app_active)
        db_session.commit()
        assert app_active.is_complete is False

        # Completed application
        app_complete = Application(job_id="job1", status="completed")
        db_session.add(app_complete)
        db_session.commit()
        assert app_complete.is_complete is True

        # Failed application
        app_failed = Application(job_id="job1", status="failed")
        db_session.add(app_failed)
        db_session.commit()
        assert app_failed.is_complete is True

    def test_application_requires_action(self, db_session):
        """Test intervention requirement check"""
        job = Job(
            id="job1",
            url="https://test.com",
            company="Corp",
            title="Role",
            location="City",
            source="linkedin"
        )
        db_session.add(job)
        db_session.commit()

        app = Application(
            job_id="job1",
            status="paused",
            user_intervention_required=True,
            intervention_reason="Login required"
        )
        db_session.add(app)
        db_session.commit()

        assert app.requires_action is True


class TestApplicationLogModel:
    """Test ApplicationLog model"""

    def test_create_application_log(self, db_session):
        """Test creating an application log entry"""
        job = Job(
            id="job1",
            url="https://test.com",
            company="Corp",
            title="Role",
            location="City",
            source="linkedin"
        )
        db_session.add(job)
        db_session.commit()

        app = Application(job_id="job1", status="applying")
        db_session.add(app)
        db_session.commit()

        log = ApplicationLog(
            application_id=app.id,
            event_type="started",
            message="Application started"
        )
        db_session.add(log)
        db_session.commit()

        retrieved = db_session.query(ApplicationLog).first()
        assert retrieved is not None
        assert retrieved.event_type == "started"
        assert retrieved.application_id == app.id

    def test_log_event_factory(self, db_session):
        """Test ApplicationLog factory method"""
        job = Job(
            id="job1",
            url="https://test.com",
            company="Corp",
            title="Role",
            location="City",
            source="linkedin"
        )
        db_session.add(job)
        db_session.commit()

        app = Application(job_id="job1", status="applying")
        db_session.add(app)
        db_session.commit()

        # Use factory method
        log = ApplicationLog.log_event(
            application_id=app.id,
            event_type="field_filled",
            message="Name field filled",
            event_metadata={"field_name": "name", "value": "John Doe"}
        )
        
        assert log.event_type == "field_filled"
        assert log.event_metadata["field_name"] == "name"


class TestRelationships:
    """Test model relationships"""

    def test_job_has_many_applications(self, db_session):
        """Test that a job can have multiple applications"""
        job = Job(
            id="job1",
            url="https://test.com",
            company="Corp",
            title="Role",
            location="City",
            source="linkedin"
        )
        db_session.add(job)
        db_session.commit()

        # Create multiple applications for same job
        app1 = Application(job_id="job1", status="queued")
        app2 = Application(job_id="job1", status="applying")
        db_session.add_all([app1, app2])
        db_session.commit()

        retrieved_job = db_session.query(Job).filter_by(id="job1").first()
        assert len(retrieved_job.applications) == 2

    def test_application_has_many_logs(self, db_session):
        """Test that an application can have multiple logs"""
        job = Job(
            id="job1",
            url="https://test.com",
            company="Corp",
            title="Role",
            location="City",
            source="linkedin"
        )
        db_session.add(job)
        db_session.commit()

        app = Application(job_id="job1", status="applying")
        db_session.add(app)
        db_session.commit()

        # Add multiple logs
        logs = [
            ApplicationLog(application_id=app.id, event_type="started", message="Start"),
            ApplicationLog(application_id=app.id, event_type="field_filled", message="Fill"),
            ApplicationLog(application_id=app.id, event_type="completed", message="Done"),
        ]
        db_session.add_all(logs)
        db_session.commit()

        retrieved_app = db_session.query(Application).filter_by(id=app.id).first()
        assert len(retrieved_app.logs) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
