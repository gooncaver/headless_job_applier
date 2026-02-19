"""SQLAlchemy ORM Models for Headless Job Applier"""

from datetime import datetime, timedelta
from typing import Optional, List
import hashlib
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, ForeignKey, JSON, Index, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Job(Base):
    """Job posting entity"""
    __tablename__ = "jobs"

    id = Column(String(16), primary_key=True, index=True)
    url = Column(String(2048), unique=True, nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    html_content = Column(Text, nullable=True)  # Gzipped if large
    source = Column(String(50), nullable=False, index=True)  # linkedin, indeed, jobstreet
    scraped_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    keywords_match = Column(JSON, nullable=True)  # Array of matched keywords
    
    # Relationships
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    
    # Unique constraint on composite key
    __table_args__ = (
        UniqueConstraint('company', 'title', 'location', name='unique_job_posting'),
        Index('idx_job_scraped_source', 'scraped_at', 'source'),
    )

    def __repr__(self) -> str:
        return f"Job(id={self.id}, company={self.company}, title={self.title}, location={self.location})"

    @staticmethod
    def generate_id(url: str, company: str, title: str, location: str) -> str:
        """Generate deterministic ID from job attributes for deduplication"""
        key = f"{url}|{company}|{title}|{location}".lower()
        return hashlib.sha256(key.encode()).hexdigest()[:16]

    def is_stale(self, days: int = 7) -> bool:
        """Check if job posting is older than specified days"""
        threshold = datetime.utcnow() - timedelta(days=days)
        return self.scraped_at < threshold


class Application(Base):
    """Job application tracking"""
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column(String(16), ForeignKey("jobs.id"), nullable=False, index=True)
    status = Column(
        String(50),
        nullable=False,
        index=True,
        default="queued"
        # Possible values: queued, customizing, ready, applying, completed, failed, paused
    )
    tailored_resume_path = Column(String(512), nullable=True)
    cover_letter_path = Column(String(512), nullable=True)
    application_url = Column(String(2048), nullable=True)
    applied_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    user_intervention_required = Column(Boolean, default=False)
    intervention_reason = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", back_populates="applications")
    logs = relationship("ApplicationLog", back_populates="application", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Application(id={self.id}, job_id={self.job_id}, status={self.status})"

    @property
    def is_complete(self) -> bool:
        """Check if application is in a terminal state"""
        return self.status in ["completed", "failed", "paused"]

    @property
    def requires_action(self) -> bool:
        """Check if application requires user intervention"""
        return self.user_intervention_required or self.status == "paused"


class ApplicationLog(Base):
    """Audit trail for application attempts"""
    __tablename__ = "application_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False)
    # Possible values: started, field_filled, file_uploaded, screenshot, error, completed, paused
    message = Column(Text, nullable=False)
    event_metadata = Column(JSON, nullable=True)  # Additional context (renamed from 'metadata' - reserved in SQLAlchemy)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    application = relationship("Application", back_populates="logs")

    def __repr__(self) -> str:
        return f"ApplicationLog(id={self.id}, application_id={self.application_id}, event_type={self.event_type})"

    @staticmethod
    def log_event(
        application_id: int,
        event_type: str,
        message: str,
        event_metadata: Optional[dict] = None
    ) -> "ApplicationLog":
        """Factory method to create and return a log entry"""
        log = ApplicationLog(
            application_id=application_id,
            event_type=event_type,
            message=message,
            event_metadata=event_metadata or {}
        )
        return log
