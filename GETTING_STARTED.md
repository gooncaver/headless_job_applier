# Getting Started - Headless Job Applier

**Last Updated**: February 18, 2026  
**Current Phase**: 1 - Foundation & Scraper (Week 1 Complete ✅)

---

## 🎯 Current Status

✅ **Week 1 - Project Setup & Database**: COMPLETE
- Project structure established
- Database models implemented and tested
- CLI entry point created
- Documentation complete

🔴 **Week 2-3 - Browser Automation & Scraping**: NOT STARTED
- Implement Playwright browser manager
- Create job scrapers for LinkedIn, Indeed, Jobstreet
- Set up CrewAI agent orchestration

---

## 📋 Next Steps to Get Started

### Step 1: Install Dependencies (if not done via setup.bat)

```bash
# Activate virtual environment (first time)
venv\Scripts\activate.bat

# Or if already activated, install requirements
pip install -r requirements.txt

# Install development dependencies (optional, for testing)
pip install -r requirements-dev.txt
```

### Step 2: Configure Your Environment

```bash
# Copy .env template
copy .env.example .env

# Edit .env with your credentials
# Required:
# - ANTHROPIC_API_KEY (Claude API)
# - LINKEDIN_EMAIL & PASSWORD
# - INDEED_EMAIL & PASSWORD
# - JOBSTREET_EMAIL & PASSWORD
# - MAILGUN_API_KEY (for notifications)
# - ENCRYPTION_KEY (see next step)

# Generate encryption key for credentials
python src/main.py generate-key

# Copy the output and add to .env as:
# ENCRYPTION_KEY=<generated_key>
```

### Step 3: Update Your Profile

```bash
# Edit input/user_profile.yaml with your:
# - Personal information (name, email, phone)
# - Work experience
# - Education
# - Technical skills
# - Career preferences

# This file is used for:
# - Resume customization (matching job descriptions)
# - Automated form filling (name, email, experience, etc.)
# - Cover letter generation (if enabled)
```

### Step 4: Initialize Database

```bash
# Create database tables
python src/main.py init-db-cmd

# Verify database is working
python src/main.py test-db

# Check status
python src/main.py status
```

---

## 🧪 Verify Phase 1 Completion

Run the verification script to confirm everything is set up correctly:

```bash
python verify_phase1.py
```

Expected output:
```
🔍 Verifying project structure...
  ✓ src/
  ✓ config/
  ...

✅ Phase 1 Verification Complete - All checks passed!
```

Or run individual tests:

```bash
# Test database models
pytest tests/test_database.py -v

# Test with coverage
pytest tests/test_database.py --cov=src --cov-report=html
```

---

## 📚 Available Commands

```bash
# Show help
python src/main.py --help

# Application setup
python src/main.py setup                  # Full initialization
python src/main.py init-db-cmd          # Create database
python src/main.py test-db               # Health check
python src/main.py generate-key          # Generate encryption key

# Status & Management
python src/main.py status                # Show statistics
python src/main.py reset-db              # WARNING: Delete all data

# Phase implementations (stubs - not implemented yet)
python src/main.py scrape                # Job scraping (Week 2)
python src/main.py customize             # Resume customization (Week 4)
python src/main.py apply                 # Application automation (Week 6)
```

---

## 📁 Key Files to Know

### Configuration
- `config/config.yaml` - Application settings (search keywords, LLM settings, etc.)
- `input/user_profile.yaml` - Your personal and professional information
- `.env` - Environment variables and secrets (gitignored)

### Database
- `database/jobs.db` - SQLite database (gitignored, created at runtime)
- `src/database/models.py` - ORM model definitions
- `src/database/engine.py` - Database connection management

### Code
- `src/main.py` - CLI entry point
- `src/utils/credentials.py` - Credential encryption
- `src/utils/logging_config.py` - Logging setup
- `src/database/` - Database layer

### Testing
- `tests/test_database.py` - Database model tests (40+ test cases)
- `verify_phase1.py` - Phase 1 verification script

### Documentation
- `README.md` - Comprehensive project guide
- `PHASE1_SUMMARY.md` - Week 1 completion report
- `docs/design.md` - Complete system architecture
- `docs/roadmap.md` - 12-week implementation plan
- `docs/changelog.md` - Version history

---

## 🚀 Phase 1 - Week 1 Achievements

✅ Created 15+ directories with proper structure  
✅ Implemented SQLAlchemy ORM models (Job, Application, ApplicationLog)  
✅ Built database engine with session management  
✅ Created credential encryption system  
✅ Set up structured logging infrastructure  
✅ Designed CLI with 8 commands  
✅ Wrote 40+ database model tests  
✅ Created setup automation scripts  
✅ Wrote comprehensive documentation  

---

## 📅 What's Next (Phase 1 - Weeks 2-3)

### Week 2: Browser Automation
- [ ] Implement Playwright browser manager
- [ ] Create session save/restore functions
- [ ] Test on Books to Scrape practice site
- [ ] Handle browser context management

### Week 3: Job Scrapers
- [ ] Build LinkedIn scraper
- [ ] Build Indeed scraper
- [ ] Build Jobstreet scraper
- [ ] Implement CrewAI agent orchestration
- [ ] Set up APScheduler for daily jobs

### Verification Gate 2
✓ Successfully scrape 10+ jobs from 1 portal with no duplicates

---

## 💡 Pro Tips

### Database Inspection
```bash
# Open database directly
sqlite3 database/jobs.db

# View tables
.tables

# Query jobs
SELECT COUNT(*) FROM jobs;
SELECT * FROM jobs LIMIT 5;

# Exit
.exit
```

### Debugging
```bash
# Enable debug logging
set DEBUG=true
python src/main.py status

# Or in code:
# from src.utils.logging_config import logger
# logger.debug("Debug message")
```

### Development Workflow
```bash
# Activate environment first
venv\Scripts\activate.bat

# Run commands
python src/main.py ...

# Deactivate when done
deactivate
```

---

## ⚠️ Important Notes

### Security
- **Never commit**: `.env`, `database/jobs.db`, `*.pdf` files, `logs/`
- **Always use**: Encrypted credentials in `config/encrypted_creds.json`
- **Keep safe**: Your `ENCRYPTION_KEY` environment variable

### Credentials
- LinkedIn, Indeed, Jobstreet credentials are stored encrypted
- Mailgun API key used for email notifications
- Claude/OpenAI API keys for LLM operations

### Database
- SQLite by default (can upgrade to PostgreSQL later)
- Jobs deduplicated by: URL, Company, Title, Location
- Applications track status through 7 states
- All changes are logged in ApplicationLog

---

## 🐛 Troubleshooting

**"Cannot find module 'src'"**
- Make sure you're in the project root directory
- Check that `src/__init__.py` exists

**"ENCRYPTION_KEY not found"**
- Run: `python src/main.py generate-key`
- Add the output to `.env`

**"Database is locked"**
- Close any overlapping applications
- Delete `database/jobs.db` and recreate

**"Playwright not found"**
- Run: `playwright install chromium`
- Or reinstall: `pip install --force-reinstall playwright`

---

## 📞 Getting Help

1. **Check README.md** - Comprehensive setup guide
2. **Read design.md** - Architecture and design decisions
3. **Run verify_phase1.py** - Identify what's wrong
4. **Check logs/** - Review error logs
5. **Read docs/** - Look for relevant documentation

---

## ✅ Setup Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Requirements installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with credentials
- [ ] `input/user_profile.yaml` filled out
- [ ] Database initialized (`python src/main.py init-db-cmd`)
- [ ] Database verified (`python src/main.py test-db`)
- [ ] Verification script passed (`python verify_phase1.py`)

Once all checked, you're ready for Phase 1 - Week 2! 🚀

---

**Next Phase**: Week 2 - Browser Automation & Scraper Implementation  
**Estimated Start**: Next working day  
**Estimated Duration**: 2 weeks until Verification Gate achieved
