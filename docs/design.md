# Headless Job Applier - System Design Document

**Version**: 1.0.0  
**Last Updated**: February 19, 2026  
**Status**: Phase 1 Week 1 Complete - Database Foundation ✅

---

## Executive Summary

A three-phase, locally-run job automation pipeline for Windows that:
1. **Scraper**: Daily fetches jobs from LinkedIn/Indeed/Jobstreet using CrewAI + Playwright
2. **Resume Customizer**: AI-tailors markdown resume to each job description, exports to PDF
3. **Application Filler**: Automates form filling with Playwright, handles exceptions with user notifications

**Core Technology**: Playwright, CrewAI, OpenAI GPT-4o API, SQLAlchemy ORM, APScheduler, WeasyPrint  
**Deployment**: Local Windows laptop with Task Scheduler  
**Database**: SQLite (local)

---

## Implementation Status

**Phase 1 Week 1 - Foundation** ✅ COMPLETE

| Component | Status | Details |
|-----------|--------|---------|
| **Database Layer** | ✅ Complete | SQLAlchemy 2.0.33, SQLite, 3 tables, 13 unit tests passing |
| **ORM Models** | ✅ Complete | Job, Application, ApplicationLog with relationships |
| **Database Engine** | ✅ Complete | Session management, health checks, statistics queries |
| **Configuration** | ✅ Complete | config.yaml, user_profile.yaml templates |
| **Encryption** | ✅ Complete | Fernet-based credential manager |
| **Logging** | ✅ Complete | loguru with rotation, retention, multiple channels |
| **CLI Framework** | ✅ Complete | Click framework with 9 commands |
| **Testing** | ✅ Complete | 13/13 unit tests passing, verification script 5/5 checks |
| **Documentation** | ✅ Complete | Comprehensive docs, roadmap, bug tracking |
| **Dependency Management** | ✅ Complete | 40+ packages installed, Python 3.13.1 compatible |

**Phase 1 Week 2-3** 🔴 Not Started
- Playwright browser automation
- Site-specific scrapers (LinkedIn, Indeed, Jobstreet)
- CrewAI agent orchestration
- APScheduler integration

**Key Achievements**:
- 🟢 All Phase 1 Week 1 deliverables complete
- 🟢 5/5 verification checks passing
- 🟢 13/13 unit tests passing
- 🟢 Python 3.13.1 compatibility resolved
- 🟢 SQLAlchemy 2.0 compatibility issues fixed
- 🟢 LLM provider updated to OpenAI GPT-4o

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Daily Scheduled Job (Windows Task Scheduler @ 6 AM)         │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────▼────────────┐
        │  PART 1: SCRAPER    │
        │  (CrewAI + Playwright)
        │  • LinkedIn jobs    │
        │  • Indeed jobs      │
        │  • Jobstreet jobs   │
        │  ▼ Dedup by URL/    │
        │    Company/Title    │
        │  ▼ Save to SQLite   │
        └────────┬────────────┘
                 │
        ┌────────▼──────────────────┐
        │  DATABASE (SQLite)        │
        │  tables:                  │
        │  • jobs (URL, company,    │
        │    title, location, desc) │
        │  • applications (status,  │
        │    tailored_resume_path)  │
        └────────┬──────────────────┘
                 │
        ┌────────▼──────────────────┐
        │  PART 2: CLI SELECTOR     │
        │  User selects jobs to     │
        │  apply for (CLI menu)     │
        └────────┬──────────────────┘
                 │
        ┌────────▼───────────────────┐
        │  PART 2: CUSTOMIZER        │
        │  (OpenAI GPT-4o + WeasyPrint) │
        │  • Compare job desc ↔ resume
        │  • AI-tailor resume        │
        │  • Markdown → PDF          │
        │  ▼ Save to output/         │
        │    {company}/{date}/       │
        └────────┬───────────────────┘
                 │
        ┌────────▼────────────────────┐
        │  PART 3: APPLIER           │
        │  (Playwright + AI Agent)    │
        │  • Load job posting URL    │
        │  • Fill form fields (AI)   │
        │  • Upload tailored resume  │
        │  • [Optional] Upload       │
        │    cover letter (AI gen'd) │
        │  ▼ Email notify or pause   │
        │    for manual intervention │
        └────────┬────────────────────┘
                 │
        ┌────────▼────────────────────┐
        │  OUTPUT                    │
        │  • Applications log        │
        │  • Tailored resumes/ PDFs  │
        │  • Email notifications    │
        │    (success / blocked)     │
        └────────────────────────────┘
```

---

## Technical Stack

### Core Dependencies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Scheduling** | APScheduler | 3.10+ | Daily scraping jobs |
| **Task Scheduler** | Windows Task Scheduler | Built-in | OS-level scheduling |
| **Web Scraping** | Playwright | 1.45+ | Headless browser automation |
| **Agent Framework** | CrewAI | 0.50+ | Multi-agent orchestration |
| **Agent Tools** | crewai-tools | 0.4+ | Browser/web tools integration |
| **Browser AI** | browser-use | 0.5+ | AI-powered Playwright wrapper |
| **Database ORM** | SQLAlchemy | 2.0.33 ✅ | Database abstraction |
| **Database** | SQLite | 3.40+ | Local data storage |
| **Data Validation** | Pydantic | 2.9.2 ✅ | Type-safe models |
| **LLM API** | OpenAI SDK | 1.10.0 ✅ | Primary: GPT-4o API client |
| **LLM Fallback** | Anthropic SDK | 0.25.9 | Alternative: Claude API (optional) |
| **YAML Parser** | ruamel.yaml | 0.18.6 ✅ | YAML config parsing (PyYAML alternative) |
| **PDF Generation** | WeasyPrint | 60+ | Markdown → PDF conversion |
| **PDF Manipulation** | pypdf | 4.0+ | PDF utilities |
| **HTML Parsing** | BeautifulSoup4 | 4.12.3 ✅ | HTML extraction |
| **HTTP Client** | httpx | 0.25.2 ✅ | Async HTTP requests |
| **Markdown** | markdown | 3.5.2 ✅ | Markdown parsing |
| **Encryption** | cryptography | 42.0.7 ✅ | Credential encryption |
| **Email** | mailgun-sdk | 1.0+ | Notification emails |
| **CLI Framework** | click | 8.1.7 ✅ | Command-line interface |
| **Logging** | loguru | 0.7.2 ✅ | Structured logging |
| **Scheduling Utils** | python-dateutil | 2.8.2 ✅ | Date/time handling |
| **Retry Logic** | tenacity | 8.2.3 ✅ | Exponential backoff |
| **Database Migrations** | alembic | 1.13.1 ✅ | Schema versioning |
| **Job Scheduling** | apscheduler | 3.10.4 ✅ | APScheduler integration |

### Development Dependencies

- pytest 8.0.0 ✅
- pytest-cov 4.1.0 ✅
- pytest-asyncio 0.23+ (for async tests)
- black (code formatting - optional)
- flake8 (linting - optional)
- mypy (type checking - optional)

---

## Project Structure

```
headless_job_applier/
├── config/
│   ├── config.yaml              # User credentials, API keys
│   ├── encrypted_creds.json     # Encrypted passwords (gitignored)
│   └── schema.md                # Config validation docs
├── src/
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── browser_manager.py   # Playwright session handling
│   │   ├── sites/
│   │   │   ├── __init__.py
│   │   │   ├── linkedin_scraper.py
│   │   │   ├── indeed_scraper.py
│   │   │   └── jobstreet_scraper.py
│   │   ├── deduplicator.py      # Hash-based job dedup
│   │   ├── crewai_orchestrator.py  # CrewAI agents
│   │   └── scheduler.py         # APScheduler integration
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   ├── engine.py            # SQLite session management
│   │   └── migrations/          # Alembic migrations (optional)
│   ├── customizer/
│   │   ├── __init__.py
│   │   ├── template_manager.py  # Multi-template management & recommendations
│   │   ├── resume_customizer.py # Resume customization orchestration
│   │   ├── resume_parser.py     # Parse markdown resume
│   │   ├── claude_interface.py  # Claude API integration
│   │   ├── pdf_generator.py     # Markdown → PDF
│   │   └── cover_letter_generator.py  # Optional cover letters
│   ├── applier/
│   │   ├── __init__.py
│   │   ├── form_filler.py       # AI-powered form filling
│   │   ├── session_manager.py   # Auth + session persistence
│   │   └── error_handler.py     # Retry + user notifications
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── credentials.py       # Credential encryption
│   │   ├── notifications.py     # Email alerts
│   │   ├── logging_config.py    # Structured logging
│   │   ├── cli.py               # CLI interface
│   │   └── status_tracker.py    # Application status tracking
│   └── main.py                  # Entry point
├── input/
│   ├── resume.md                # User's resume (provided)
│   └── user_profile.yaml        # User template (to fill)
├── output/
│   └── resumes/                 # {company}/{date}/resume.pdf
├── database/
│   └── jobs.db                  # SQLite DB (gitignored)
├── logs/                        # Execution logs (gitignored)
│   ├── scraper/
│   ├── customizer/
│   └── applier/
├── tests/
│   ├── __init__.py
│   ├── test_scraper.py
│   ├── test_customizer.py
│   ├── test_applier.py
│   └── fixtures/
├── docs/
│   ├── design.md                # This file
│   ├── roadmap.md               # Implementation roadmap
│   ├── bugfixes.md              # Bug tracking
│   └── changelog.md             # Version history
├── requirements.txt             # Python dependencies
├── requirements-dev.txt         # Dev dependencies
├── .gitignore                   # Git exclusions
├── .env.example                 # Template for secrets
├── setup.ps1                    # Windows setup script
└── README.md                    # User documentation
```

---

## Database Schema

### Jobs Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | SHA-256 hash of (url, company, title, location) |
| url | TEXT | UNIQUE NOT NULL | Job posting URL |
| company | TEXT | NOT NULL | Company name |
| title | TEXT | NOT NULL | Job title |
| location | TEXT | NOT NULL | Job location (remote, city, etc.) |
| description | TEXT | - | Full job description |
| html_content | BLOB | - | Gzipped HTML |
| source | TEXT | NOT NULL | 'linkedin', 'indeed', 'jobstreet' |
| scraped_at | TIMESTAMP | DEFAULT NOW | First scrape timestamp |
| updated_at | TIMESTAMP | DEFAULT NOW | Last update timestamp |
| keywords_match | TEXT | - | JSON array of matched keywords |

**Indexes**:
- UNIQUE(url)
- UNIQUE(company, title, location)
- INDEX(scraped_at)
- INDEX(source)

### Applications Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Application ID |
| job_id | TEXT | FOREIGN KEY(jobs.id) | Reference to job |
| status | TEXT | NOT NULL | 'queued', 'customizing', 'ready', 'applying', 'completed', 'failed' |
| resume_template | TEXT | - | Template used (e.g., 'resume_consultant.md') |
| tailored_resume_path | TEXT | - | Path to generated PDF |
| cover_letter_path | TEXT | - | Path to cover letter PDF (optional) |
| application_url | TEXT | - | Actual application form URL |
| applied_at | TIMESTAMP | - | Submission timestamp |
| error_message | TEXT | - | Failure reason if status='failed' |
| created_at | TIMESTAMP | DEFAULT NOW | Queue timestamp |

**Indexes**:
- INDEX(job_id)
- INDEX(status)

### ApplicationLog Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Log entry ID |
| application_id | INTEGER | FOREIGN KEY(applications.id) | Reference to application |
| event_type | TEXT | NOT NULL | 'started', 'field_filled', 'file_uploaded', 'error', 'completed' |
| message | TEXT | NOT NULL | Event description |
| metadata | TEXT | - | JSON metadata |
| timestamp | TIMESTAMP | DEFAULT NOW | Event timestamp |

---

## Configuration Management

### config.yaml Structure

```yaml
# Job Search Parameters
search:
  keywords:
    - "data engineer"
    - "consultant"
    - "data scientist"
    - "forward deployed engineer"
    - "solution architect"
  required_keywords:
    - "Palantir Foundry"
  locations:
    - "remote"
    - "Bay Area"
    - "Singapore"
  job_level: "mid-level"  # junior, mid-level, senior

# Portal Credentials (references encrypted store)
portals:
  linkedin:
    enabled: true
    email: ${LINKEDIN_EMAIL}
    password: ${LINKEDIN_PASSWORD}
  indeed:
    enabled: true
    email: ${INDEED_EMAIL}
    password: ${INDEED_PASSWORD}
  jobstreet:
    enabled: true
    email: ${JOBSTREET_EMAIL}
    password: ${JOBSTREET_PASSWORD}

# LLM Configuration
llm:
  provider: "openai"  # openai (primary), anthropic (fallback)
  model: "gpt-4o"  # OpenAI primary model
  api_key: ${OPENAI_API_KEY}
  temperature: 0.2
  max_tokens: 4096

# Alternative: Anthropic/Claude Configuration (Optional)
# llm:
#   provider: "anthropic"  # anthropic
#   model: "claude-3-5-sonnet-20241022"
#   api_key: ${ANTHROPIC_API_KEY}
#   temperature: 0.2
#   max_tokens: 2000

# Email Notifications
notifications:
  email:
    provider: "mailgun"  # mailgun, sendgrid, smtp
    api_key: ${MAILGUN_API_KEY}
    sender: "noreply@yourdomain.com"
    recipient: "your@email.com"
  enabled_events:
    - "login_required"
    - "application_complete"
    - "application_failed"

# Automation Settings
automation:
  headless: true
  slow_motion_ms: 100  # Delay between actions (for debugging)
  timeout_seconds: 30
  screenshot_on_error: true
  max_retries: 3
  retry_delay_seconds: 5

# Resume Customization
customization:
  generate_cover_letters: false  # Per-application override
  cover_letter_tone: "professional"
  pdf_style: "simple"  # simple, professional

# Scheduling
scheduling:
  scrape_time: "06:00"  # 24-hour format
  scrape_frequency: "daily"
```

### user_profile.yaml Structure

```yaml
# Personal Information
personal:
  name: "Your Full Name"
  email: "your.email@domain.com"
  phone: "+65 1234 5678"
  location: "Singapore"
  linkedin_url: "https://linkedin.com/in/yourprofile"

# Professional Summary
summary: |
  Brief professional summary that will be tailored per job.
  Keep this generic; AI will customize it.

# Work History (for form filling)
work_experience:
  - company: "Palantir Technologies"
    title: "Forward Deployed Engineer"
    start_date: "2024-05"
    end_date: "Present"
    current: true
    description: |
      Led development of AI applications for semiconductor clients.
      Expertise in Palantir Foundry platform.
  
  - company: "Rightship"
    title: "Machine Learning Engineer"
    start_date: "2023-04"
    end_date: "2024-05"
    current: false
    description: |
      Rewrote ML pipelines for production using Spark and Azure.

# Education
education:
  - degree: "Masters in Computing"
    university: "National University of Singapore"
    graduation_year: 2025
    gpa: "4.5/5.0"
  
  - degree: "Bachelor of Business Administration"
    university: "National University of Singapore"
    graduation_year: 2019
    gpa: "4.5/5.0"

# Skills (prioritized list - most relevant first)
skills:
  technical:
    - "Palantir Foundry"
    - "Python"
    - "Data Engineering"
    - "Apache Spark"
    - "Machine Learning"
    - "Cloud Computing (Azure, AWS)"
    - "SQL"
    - "Distributed Systems"
  
  soft:
    - "Technical Leadership"
    - "Client Engagement"
    - "Solution Architecture"

# Certifications
certifications:
  - name: "AWS Certified Solutions Architect"
    issuer: "Amazon"
    year: 2023

# Application Preferences
preferences:
  preferred_roles:
    - "Data Engineer"
    - "Solution Architect"
    - "Forward Deployed Engineer"
    - "Machine Learning Engineer"
  
  remote_preference: "remote"  # remote, hybrid, onsite
  willing_to_relocate: false
  expected_salary_min: 120000  # USD/year
  notice_period_days: 30
```

---

## Deduplication Strategy

**Primary Key**: SHA-256 hash of `{url}|{company}|{title}|{location}` (case-insensitive)

**Algorithm**:
```python
import hashlib

def generate_job_id(url: str, company: str, title: str, location: str) -> str:
    key = f"{url}|{company}|{title}|{location}".lower()
    return hashlib.sha256(key.encode()).hexdigest()[:16]
```

**Staleness Check**: Re-scrape jobs older than 7 days to update descriptions.

---

## CrewAI Agent Architecture

### Agent Definitions

#### 1. Scraper Agent
- **Role**: Web Content Scraper
- **Goal**: Extract clean job listings from job portals
- **Tools**: `scrape_linkedin`, `scrape_indeed`, `scrape_jobstreet`
- **Backstory**: Expert at navigating complex websites and avoiding bot detection

#### 2. Extractor Agent
- **Role**: Data Analyst
- **Goal**: Parse unstructured HTML → structured JSON
- **Tools**: `beautifulsoup_parser`, `regex_extractor`
- **Backstory**: Specialist in extracting structured data from messy content

#### 3. Deduplicator Agent
- **Role**: Data Quality Specialist
- **Goal**: Identify and filter duplicate job postings
- **Tools**: `database_lookup`, `hash_generator`
- **Backstory**: Ensures database integrity with composite key matching

### Task Flow

```
Task 1: Scraping
  ↓ (Raw HTML from 3 portals)
Task 2: Extraction
  ↓ (Structured JSON: {url, company, title, location, description})
Task 3: Deduplication
  ↓ (Unique jobs only)
Database Insert
```

---

## Resume Customization Architecture

### Multi-Template System

The customizer supports multiple resume templates optimized for different job types:

| Template | Target Roles | Focus | Keywords |
|----------|-------------|-------|----------|
| `resume_consultant.md` | Consultant, Manager, Business Analyst | Client engagement, strategy, leadership | consulting, strategy, project management |
| `resume_solution_architect.md` | Solution Architect, Tech Lead, Enterprise Architect | System design, architecture, enterprise solutions | architecture, enterprise, microservices |
| `resume_data_engineer.md` | Data Engineer, ETL Developer, Analytics Engineer | Data pipelines, big data, infrastructure | pipeline, etl, spark, hadoop, analytics |
| `resume_fde.md` | Full-Stack Developer, Frontend Engineer, Web Developer | Development, technical skills, frameworks | developer, react, node, typescript, web |

### Template Selection Logic

The `TemplateManager` recommends templates using a scoring system:

1. **Role Matching** (+10 points): Job title contains target role
   - "Solution Architect" position → recommend `resume_solution_architect.md`
2. **Keyword Matching** (+2 points per keyword): Keywords appear in job description
   - "big data pipeline development" → recommend `resume_data_engineer.md`
3. **Priority Boost** (varies): Built-in template priority
   - Higher priority = first recommendation when tied

### Customizer Components

**TemplateManager** (`src/customizer/template_manager.py`):
- Registry of 4 resume templates with metadata
- Keyword-based recommendation engine
- Template loading and validation
- CLI prompt generation for user selection

**ResumeCustomizer** (`src/customizer/resume_customizer.py`):
- Template selection for specific jobs
- Output path management (organized by company)
- Resume content preparation for AI processing
- Application-level template tracking

### Data Flow

```
Job Posting (title + description)
    ↓
TemplateManager.recommend_templates()
    ↓
[ranked list of templates]
    ↓
User selects template (or auto-choose top recommendation)
    ↓
ResumeCustomizer.customize_resume()
    ↓
Template content + job info prepared
    ↓
AI customization (Phase 2, Week 4)
    ↓
Tailored resume stored at: output/resumes/{company}/{date}_{template_type}.md
```

### Benefits of Multi-Template Approach

1. **Role-Specific Emphasis**: Each template emphasizes relevant experiences
2. **Better AI Tailoring**: Focused starting point for customization
3. **User Choice**: Allows manual override if preferences change
4. **Extensibility**: Easy to add new templates for new role types
5. **Tracking**: Database records which template was used per application

---

## Resume Customization Workflow

### Phase 1: Parsing Original Resume
```python
class Resume(BaseModel):
    name: str
    email: str
    phone: str
    summary: str
    experiences: List[Experience]
    education: List[Education]
    skills: List[str]
    certifications: List[str]
```

### Phase 2: AI Tailoring (Claude Prompt)
```
System: You are an expert resume consultant for tech roles.

User:
ORIGINAL RESUME:
{resume_markdown}

TARGET JOB DESCRIPTION:
{job_description}

TASK:
1. Extract 5 core requirements from job description
2. Reorder candidate's skills (most relevant first)
3. Highlight 2-3 experiences that match requirements
4. Adapt summary to emphasize relevant background
5. Return JSON with tailored resume

CONSTRAINTS:
- Do NOT fabricate experience
- Keep under 1 page
- Maintain professional tone
- Emphasize Palantir Foundry if mentioned in job
```

### Phase 3: PDF Generation
- **Method**: WeasyPrint (HTML → PDF)
- **Template**: Simple CSS styling (margins, fonts, headings)
- **Output Path**: `output/resumes/{company}/{YYYY-MM-DD}/resume_tailored.pdf`

---

## Application Automation Strategy

### Browser Session Management
- **Storage**: Save cookies + localStorage as JSON (`storage_state`)
- **Reuse**: Load saved state for authenticated portals
- **Expiry**: Re-authenticate if session expired (redirect to login)

### AI Form Filling Pattern
```python
from browser_use import Agent

agent = Agent(
    task=f"""
    Complete job application at {url}:
    - Fill name, email, phone from user_profile
    - Upload resume from {resume_pdf_path}
    - Answer screening questions intelligently
    - Stop before final submit (screenshot for verification)
    """,
    llm_config={"model": "claude-3-5-sonnet-20241022"}
)
```

### Error Recovery
- **Retry Logic**: Exponential backoff (1s, 2s, 4s) for network errors
- **User Intervention**: Email notification for:
  - OAuth login required (Google, LinkedIn)
  - CAPTCHA detected
  - Form structure not recognized
  - Account creation required

---

## Exception Handling

### Error Classification

```python
class ApplicationError(Exception):
    """Base exception for application system"""
    
class UserInterventionRequired(ApplicationError):
    """Requires manual user action"""
    - LoginRequired
    - CaptchaDetected
    - AccountCreationNeeded
    - FormNotRecognized

class RecoverableError(ApplicationError):
    """Can retry automatically"""
    - NetworkTimeout
    - SessionExpired
    - ElementNotFound

class ConfigurationError(ApplicationError):
    """Invalid config or missing credentials"""
```

### Account Creation Flow
1. Detect "account doesn't exist" page
2. Email user with link: "Create account at {portal}"
3. Wait 5 minutes for user action
4. Resume automation from current page
5. If timeout: Mark application as "paused"

---

## Security Considerations

### Credential Encryption
- **Method**: Cryptography library with Fernet symmetric encryption
- **Key Storage**: Environment variable `ENCRYPTION_KEY` (32 bytes)
- **Encrypted Fields**: Portal passwords, API keys
- **File**: `config/encrypted_creds.json` (gitignored)

### API Key Management
- **Primary**: Environment variables
- **Fallback**: `.env` file (gitignored)
- **Never**: Hardcoded in source

### Session Security
- **Browser State**: Stored locally in `~/.headless_job_applier/sessions/`
- **Permissions**: Restricted to current user (Windows ACLs)

---

## Performance Considerations

### Scraping Rate Limits
- **LinkedIn**: 1 request per 3 seconds (avoid blocking)
- **Indeed**: 1 request per 2 seconds
- **Jobstreet**: 1 request per 2 seconds

### Database Optimization
- **Indexes**: On (scraped_at, source, status)
- **Compression**: Gzip HTML content before storage
- **Cleanup**: Archive jobs older than 90 days

### LLM API Costs
- **Claude 3.5 Sonnet**: ~$0.003 per resume customization
- **Expected Monthly**: 100 applications × $0.003 = $0.30
- **Optimization**: Cache common job description patterns

---

## Testing Strategy

### Unit Tests
- `test_scraper.py`: Mock Playwright responses
- `test_customizer.py`: Mock Claude API
- `test_database.py`: SQLite in-memory tests

### Integration Tests
- **Scraper**: Test on Books to Scrape (practice site)
- **Form Filler**: Test on test job application forms

### End-to-End Test
1. Scrape 1 test job
2. Customize resume
3. Dry-run form filling (no submit)
4. Verify logs + PDF generated

---

## Deployment & Operations

### Initial Setup
1. Install Python 3.11+
2. `pip install -r requirements.txt`
3. Install Playwright browsers: `playwright install chromium`
4. Copy `.env.example` → `.env`, fill secrets
5. Run `python src/main.py setup` (creates DB, encrypts creds)

### Daily Operation
- **Automatic**: Windows Task Scheduler runs at 6 AM
- **Manual Check**: `python src/main.py status` (view scraped jobs)
- **Application**: `python src/main.py apply --job-ids 1,2,3`

### Monitoring
- **Logs**: `logs/scraper_YYYY-MM-DD.log`
- **Email**: Receive notifications on failures
- **DB Query**: Check application status in SQLite

---

## Future Enhancements

### Ranking System
- Score jobs by resume similarity (0-100)
- Prioritize "Palantir Foundry" mentions
- Auto-apply to top 10% matches

### Dynamic Learning
- **Troubleshooting Checklist**: Extend system prompt when user intervenes
- **Success Patterns**: Record which form-filling strategies work
- **Error Analytics**: Dashboard of common failure modes

### Multi-User Support
- Web dashboard for multiple users
- Shared job database with user-specific applications

---

## Compliance & Ethics

### Ethical Considerations
- **Honesty**: Never fabricate experience in resumes
- **Transparency**: Disclose automated application if asked
- **Respect**: Follow robots.txt and portal terms of service

### Terms of Service Compliance
- **LinkedIn**: Scraping violates TOS; use with caution or via official API
- **Indeed**: Scraping allowed with rate limits
- **Jobstreet**: Review TOS before deployment

---

## Phase 1 Week 1: Learnings & Best Practices

### What Worked Well ✅

1. **Database-First Design**: ORM models before any business logic prevented structural changes later
2. **Relative Imports**: Using relative imports in packages avoids sys.path conflicts
3. **Early Testing**: Unit tests caught issues immediately (13 tests, 13 passing)
4. **Version Pinning**: Explicit version numbers made debugging dependency issues easier
5. **Modular CLI**: Click framework made adding commands trivial
6. **Encryption Foundation**: Implementing security early avoided retrofitting later

### Challenges Encountered 🔴

1. **Python 3.13 Ecosystem**: Many packages lack wheels; required version constraints and substitutions
2. **SQLAlchemy 2.0 Breaking Changes**: Reserved keywords and SQL execution changes required code updates
3. **Import Path Complexity**: Mixed absolute/relative imports caused failures in different contexts
4. **Dependency Backtracking**: pip trying 20+ pydantic versions wastedinfinite time

### Solutions Applied 💡

1. **Pre-Install Strategy**: Install pydantic==2.9.2 (with wheels) BEFORE openai to prevent backtracking
2. **Relative Imports**: Use `.models` and `.engine` instead of `src.database.models`
3. **Explicit text() Wrapper**: SQLAlchemy 2.0 requires `text()` for raw SQL
4. **Column Renaming**: Avoid reserved keywords (metadata → event_metadata)
5. **Package Substitution**: ruamel.yaml replaces PyYAML (has Python 3.13 wheels)
6. **Phase-Based Requirements**: Split requirements by phase to manage complexity

### Best Practices for Phase 2+ 📋

1. **Always test imports from both CLI and test contexts** before committing
2. **Pin all critical versions** to avoid surprise upgrades
3. **Use GitHub Actions** for multi-Python version testing (3.11, 3.12, 3.13)
4. **Validate new dependencies**: Check wheel availability before adding
5. **Run `pip install -e .`** with setuptools for better import resolution
6. **Document trade-offs**: Why we chose OpenAI over Anthropic (cost, availability, etc.)

### Architecture Decisions 🏗️

| Decision | Rationale |
|----------|-----------|
| Relative imports | Works from any context (CLI, tests, IDE) |
| SQLAlchemy ORM | Type safety, built-in relationship management |
| SQLite | No setup, portable, sufficient for single-user |
| OpenAI primary | Better Python 3.13 support, cost-effective, reliable |
| Click CLI | Simple, Pythonic, good help messages |
| loguru logging | Structured, file rotation, minimal code |
| Fernet encryption | Built-in to cryptography, simple key management |

### Technology Choices Validated  ✓

- ✅ **SQLAlchemy 2.0**: Complex enough for relationships, simple enough for small DB
- ✅ **Pydantic 2.9.2**: Type validation, JSON serialization, IDE support
- ✅ **OpenAI GPT-4o**: Faster than Claude, better Python code generation
- ✅ **Click 8.1**: Simple, well-documented, Pythonic
- ✅ **loguru**: Clean API, auto-rotation, better than logging stdlib
- ✅ **Playwright**: Reliable headless browser, good Python support

### Technical Debt Identified 📊

| Item | Severity | Plan |
|------|----------|------|
| Add type hints to all functions | Low | Week 2 |
| Implement mypy checking in CI | Low | Week 3 |
| Add API documentation | Low | Week 4 |
| Create integration tests | Medium | Phase 2 |
| Benchmark performance | Low | Phase 4 |

---

## Appendix: Key Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Daily Jobs Scraped | 20-50 | TBD |
| Deduplication Rate | >95% | TBD |
| Resume Customization Time | <30s | TBD |
| Form Filling Success Rate | >90% | TBD |
| User Intervention Rate | <10% | TBD |
| Average Application Time | 5-10 min | TBD |

---

**Document Status**: Complete ✓  
**Next Steps**: Implement Phase 1 (Scraper)
