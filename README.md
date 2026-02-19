# Headless Job Applier

Automated job scraping, resume customization, and application filling system.

## 🎯 Overview

A three-phase automation pipeline that:
1. **Scrapes** job postings from LinkedIn, Indeed, and Jobstreet
2. **Customizes** your resume for each job using AI (OpenAI GPT-4o)
3. **Applies** to jobs automatically by filling out forms

## 📋 Project Status

**Current Phase**: Phase 1 - Foundation & Scraper (Week 1-3)  
**Status**: Setup complete, database initialized, ready for scraper development  
**Last Updated**: February 18, 2026

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Windows 10/11 (or Linux/macOS with minor adjustments)
- ~2GB disk space for virtual environment and database

### Installation

1. **Clone the repository**
   ```bash
   cd c:\Users\user\OneDrive\Development\AI App Development\headless_job_applier
   ```

2. **Run setup script** (Windows)
   ```bash
   setup.bat
   ```

   Or for Linux/macOS:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   This will:
   - Create Python virtual environment
   - Install all dependencies
   - Install Playwright browsers
   - Initialize the database
   - Generate encryption key for credentials

3. **Configure credentials**
   ```bash
   # Copy template to actual .env file
   copy .env.example .env
   
   # Edit .env in your text editor and fill in:
   # - ANTHROPIC_API_KEY or OPENAI_API_KEY
   # - LINKEDIN_EMAIL, LINKEDIN_PASSWORD
   # - INDEED_EMAIL, INDEED_PASSWORD
   # - JOBSTREET_EMAIL, JOBSTREET_PASSWORD
   # - MAILGUN_API_KEY (for email notifications)
   ```

4. **Fill in your profile**
   ```bash
   # Edit input/user_profile.yaml with your information
   # This is used for form filling and resume customization
   ```

5. **Verify setup**
   ```bash
   python src/main.py status
   ```

   Expected output:
   ```
   📊 Headless Job Applier Status
   ==================================================
   Total Jobs Scraped: 0
   Total Applications: 0
   ...
   ```

## 📁 Project Structure

```
headless_job_applier/
├── src/
│   ├── database/          # SQLAlchemy ORM models & engine
│   │   ├── models.py      # Job, Application, ApplicationLog
│   │   └── engine.py      # Database connection & session management
│   ├── scraper/           # Job scraping (Week 2-3)
│   ├── customizer/        # Resume customization (Week 4-5)
│   ├── applier/           # Application automation (Week 6-8)
│   ├── utils/             # Shared utilities
│   │   ├── credentials.py # Encryption & secrets
│   │   └── logging_config.py
│   └── main.py            # CLI entry point
├── config/
│   └── config.yaml        # Application settings
├── input/
│   ├── resume.md          # Your resume (provided)
│   └── user_profile.yaml  # Your profile for form filling
├── output/
│   └── resumes/           # Generated tailored PDFs
├── database/
│   └── jobs.db            # SQLite database
├── logs/                  # Application logs
├── tests/
│   └── test_database.py   # Database model tests
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git exclusions
└── setup.bat/setup.sh    # Setup scripts
```

## 🛠️ Development Commands

### Database

```bash
# Initialize database (create tables)
python src/main.py init-db-cmd

# Show database status
python src/main.py status

# Reset database (WARNING: destructive)
python src/main.py reset-db

# Test database connectivity
python src/main.py test-db
```

### Credentials

```bash
# Generate new encryption key
python src/main.py generate-key

# Set it in your .env file:
# ENCRYPTION_KEY=<generated_key>
```

### Testing

```bash
# Run all tests
pytest

# Run database tests only
pytest tests/test_database.py -v

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_database.py::TestJobModel::test_create_job -v
```

## 🗄️ Database Schema

### Jobs Table
- `id`: SHA-256 hash of (url, company, title, location)
- `url`: Job posting URL (unique)
- `company`: Company name
- `title`: Job title
- `location`: Job location
- `description`: Full job description
- `source`: Portal (linkedin, indeed, jobstreet)
- `scraped_at`: When job was first scraped
- `keywords_match`: Matched search keywords (JSON)

### Applications Table
- `id`: Auto-increment ID
- `job_id`: Reference to Job
- `status`: Current state (queued, customizing, ready, applying, completed, failed, paused)
- `tailored_resume_path`: Path to generated PDF
- `cover_letter_path`: Path to cover letter PDF (optional)
- `error_message`: Failure reason if failed
- `created_at`: When application was queued

### ApplicationLog Table
- `id`: Auto-increment ID
- `application_id`: Reference to Application
- `event_type`: Event type (started, field_filled, file_uploaded, error, completed, paused)
- `message`: Event description
- `metadata`: Additional context (JSON)
- `timestamp`: When event occurred

## 🔐 Security

### Credential Encryption
- Credentials are encrypted using Fernet symmetric encryption
- Encryption key stored in `.env` file (gitignored)
- Never commit actual credentials to repository
- Always use `.gitignore` to exclude:
  - `.env` file
  - `database/jobs.db`
  - `config/encrypted_creds.json`
  - `*.pdf` files
  - `logs/` directory

### Best Practices
- Keep `.env` file local only
- Regenerate encryption keys periodically
- Use strong, unique portal passwords
- Never commit `.gitignore` changes

## 📚 Phase 1 Checklist

- [x] Project directory structure created
- [x] Git repository initialized with `.gitignore`
- [x] Python dependencies configured (`requirements.txt`)
- [x] SQLAlchemy ORM models defined (Job, Application, ApplicationLog)
- [x] Database engine and session management implemented
- [x] Credential encryption utility created
- [x] Logging configuration set up
- [x] Configuration templates created (`config.yaml`, `user_profile.yaml`)
- [x] Database model unit tests written
- [x] Setup scripts created (Windows `.bat` and Linux `.sh`)
- [x] CLI entry point with commands implemented
- [ ] **VERIFICATION GATE 1**: All database tests pass ✓
- [ ] **Next**: Begin Week 2 - Browser automation & scraper implementation

## ✅ Verification Checklist

Use this to verify Phase 1 is complete:

```bash
# 1. Setup runs without errors
setup.bat

# 2. Database is created
ls database/jobs.db

# 3. All tests pass
pytest tests/test_database.py -v

# 4. Status command works
python src/main.py status

# 5. Database health check passes
python src/main.py test-db
```

## 🐛 Troubleshooting

### Issue: "No module named 'src'"
**Solution**: Make sure you're running commands from the project root directory

### Issue: "ENCRYPTION_KEY not found"
**Solution**: 
```bash
python src/main.py generate-key
# Add the output to your .env file
```

### Issue: "Database is locked"
**Solution**: 
- Close any other programs accessing the database
- Delete `database/jobs.db` and recreate: `python src/main.py init-db-cmd`

### Issue: "Playwright installation failed"
**Solution**:
```bash
# Install system dependencies (Windows):
playwright install chromium

# Or reinstall:
pip install --force-reinstall playwright==1.45.0
playwright install chromium
```

## 📖 Documentation

- [System Design Document](docs/design.md) - Complete architecture
- [Implementation Roadmap](docs/roadmap.md) - 12-week plan with milestones
- [Bug Tracking](docs/bugfixes.md) - Bug reports and fixes
- [Changelog](docs/changelog.md) - Version history

## 🚢 Next Phase

**Phase 2: Resume Customization** (Weeks 4-5)
- Resume markdown parser
- Claude API integration
- PDF generation with WeasyPrint
- CLI job selector

See [Roadmap](docs/roadmap.md) for complete details.

## 📝 Notes

- This is an MVP (Minimum Viable Product) - expect rapid iterations
- Database uses SQLite for simplicity; can upgrade to PostgreSQL later
- All credentials encrypted locally; no cloud storage of secrets
- Logging to files enables debugging and audit trails

## 🤝 Contributing

When making changes:
1. Write/update tests for new features
2. Run: `pytest` to verify tests pass
3. Update documentation as needed
4. Commit with descriptive messages

## 📄 License & Terms

- **Status**: Development phase - use at your own risk
- **Responsibility**: You are responsible for compliance with job portal terms of service
- **Ethics**: Never fabricate experience; always be honest on applications

---

**Last Updated**: February 18, 2026  
**Maintained by**: Headless Job Applier Team  
**Current Version**: 1.0.0-dev
