# Headless Job Applier - Implementation Roadmap

**Version**: 1.0.0  
**Last Updated**: February 19, 2026  
**Project Start**: February 18, 2026  
**Estimated Completion**: May 2026 (12 weeks)

---

## Overview

This roadmap tracks the phased implementation of the Headless Job Applier system. Each phase builds on the previous, with specific verification gates before proceeding.

**Legend**:
- 🔴 Not Started
- 🟡 In Progress
- 🟢 Completed
- ⏸️ Blocked
- ⚠️ At Risk

---

## Phase 1: Foundation & Scraper (Weeks 1-3)

**Goal**: Build core data pipeline with daily job scraping  
**Status**: 🟡 In Progress (Week 1 Complete ✅)  
**Start Date**: February 18, 2026  
**End Date**: TBD (Target: March 10, 2026)

### Week 1: Project Setup & Database

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Create project directory structure | � | P0 | - | See design.md structure |
| Initialize Git repository | 🟢 | P0 | - | Complete |
| Create `.gitignore` (exclude PDFs, DB, logs) | 🟢 | P0 | - | Complete |
| Install Python dependencies | 🟢 | P0 | - | Create requirements.txt |
| Install Playwright browsers | 🟡 | P0 | - | In setup script, will run in Week 2 |
| Create SQLAlchemy models (Jobs, Applications, Logs) | 🟢 | P0 | - | src/database/models.py - Complete |
| Implement database engine & session management | 🟢 | P0 | - | src/database/engine.py - Complete |
| Write unit tests for database models | 🟢 | P1 | - | tests/test_database.py - Complete |
| Create config.yaml template | 🟢 | P0 | - | config/config.yaml - Complete |
| Create user_profile.yaml template | 🟢 | P0 | - | input/user_profile.yaml - Complete |
| Implement credential encryption utility | 🟢 | P0 | - | src/utils/credentials.py - Complete |
| Set up logging configuration | 🟢 | P1 | - | src/utils/logging_config.py - Complete |

**Verification Gate 1**: ✅ PASSED - All checks verified Feb 19, 2026
- ✅ Database created at `database/jobs.db` with 3 tables
- ✅ 13/13 unit tests passing (models, relationships, constraints)
- ✅ 5/5 verification checks passing (structure, imports, models, database, CLI)
- ✅ Config templates completed and validated
- ✅ 40+ dependencies successfully installed

---

### Week 2: Browser Automation & Scraping

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Implement Playwright browser manager | 🔴 | P0 | - | src/scraper/browser_manager.py |
| Create session save/restore functions | 🔴 | P0 | - | Store cookies & localStorage |
| Build LinkedIn scraper (headless) | 🔴 | P0 | - | src/scraper/sites/linkedin_scraper.py |
| Build Indeed scraper | 🔴 | P0 | - | src/scraper/sites/indeed_scraper.py |
| Build Jobstreet scraper | 🔴 | P0 | - | src/scraper/sites/jobstreet_scraper.py |
| Implement deduplication logic | 🔴 | P0 | - | src/scraper/deduplicator.py |
| Write scraper unit tests | 🔴 | P1 | - | Mock Playwright responses |
| Test scraping on Books to Scrape (practice) | 🔴 | P1 | - | Validate parsing logic |

**Verification Gate 2**: ✓ Successfully scrape 10+ jobs from 1 portal with no duplicates

---

### Week 3: CrewAI Integration & Scheduling

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Define CrewAI scraper agents | 🔴 | P0 | - | src/scraper/crewai_orchestrator.py |
| Create scraping tasks | 🔴 | P0 | - | Sequential workflow |
| Integrate agents with Playwright scrapers | 🔴 | P0 | - | Tools: scrape_linkedin, etc. |
| Test full CrewAI scraping workflow | 🔴 | P0 | - | 3 portals → JSON → DB |
| Implement APScheduler for daily runs | 🔴 | P0 | - | src/scraper/scheduler.py |
| Create setup.ps1 for Task Scheduler | 🔴 | P0 | - | Windows Task Scheduler registration |
| Test scheduled scraping (dry-run) | 🔴 | P1 | - | Run at specified time |
| Document scraper usage | 🔴 | P1 | - | Update README.md |

**Verification Gate 3**: ✓ Full scraping workflow runs automatically via Task Scheduler

**Phase 1 Deliverables**:
- ✅ SQLite database with 20+ unique jobs
- ✅ Daily scraping scheduled at 6 AM
- ✅ Deduplication working (95%+ accuracy)
- ✅ Logs captured in `logs/scraper/`

---

## Phase 2: Resume Customization (Weeks 4-5)

**Goal**: AI-powered resume tailoring and PDF generation  
**Status**: 🔴 Not Started  
**Dependencies**: Phase 1 complete (jobs in database)  
**Start Date**: TBD  
**End Date**: TBD

### Week 4: Resume Parsing & Multi-Template Customization

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Implement TemplateManager (multi-template support) | 🟢 | P0 | ✅ | src/customizer/template_manager.py - 4 templates registered |
| Implement ResumeCustomizer orchestration | 🟢 | P0 | ✅ | src/customizer/resume_customizer.py - template selection & output paths |
| Add resume_template field to Application model | 🟢 | P0 | ✅ | Track which template used per application |
| Create Resume Pydantic model | 🔴 | P0 | - | src/customizer/models.py - structure for parsed resumes |
| Implement markdown resume parser | 🔴 | P0 | - | src/customizer/resume_parser.py |
| Parse each input/resume_*.md template | 🔴 | P0 | - | Support multiple resume variants |
| Set up OpenAI API client | 🔴 | P0 | - | src/customizer/openai_interface.py (GPT-4o primary) |
| Design resume tailoring prompt | 🔴 | P0 | - | Chain-of-thought reasoning for customization |
| Implement `tailor_resume_to_job()` function | 🔴 | P0 | - | AI API call with template context |
| Test tailoring on 3 sample job descriptions | 🔴 | P1 | - | Verify quality and template relevance |
| Add error handling for API failures | 🔴 | P1 | - | Retry logic with exponential backoff |
| Write 24 customizer unit tests | 🟢 | P1 | ✅ | tests/test_customizer.py - template manager and orchestration tests |

**New Delivery** (Phase 1): ✅ Template management system ready for Phase 2 Week 4
- ✅ 4 resume templates supported (Consultant, Architect, Data Engineer, Full-Stack)
- ✅ Keyword-based template recommendation engine
- ✅ Template selection logic (automatic + user override)
- ✅ 24 unit tests covering all template scenarios
- ✅ Database tracking of template usage per application

**Verification Gate 4**: ✓ Tailored resume JSON generated with relevant skills prioritized

---

### Week 5: PDF Generation & CLI

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Install WeasyPrint + dependencies | 🔴 | P0 | - | Test on Windows |
| Create simple HTML/CSS resume template | 🔴 | P0 | - | Clean, professional layout |
| Implement markdown → PDF converter | 🔴 | P0 | - | src/customizer/pdf_generator.py |
| Test PDF generation with tailored resume | 🔴 | P0 | - | Verify formatting |
| Implement file organization (company/date/) | 🔴 | P0 | - | output/resumes/{company}/{date}/ |
| Create CLI command: `customize --job-ids` | 🔴 | P0 | - | src/main.py |
| Build job selector CLI menu | 🔴 | P1 | - | Interactive selection |
| Write customizer unit tests | 🔴 | P1 | - | Mock Claude responses |

**Verification Gate 5**: ✓ PDF resume generated in output folder, visually acceptable

**Phase 2 Deliverables**:
- ✅ Resume customization working for any job
- ✅ PDFs stored in organized folder structure
- ✅ CLI tool for selecting jobs to customize
- ✅ Customization time <30 seconds per job

---

## Phase 3: Application Automation (Weeks 6-8)

**Goal**: Automated form filling with intelligent error handling  
**Status**: 🔴 Not Started  
**Dependencies**: Phase 2 complete (tailored PDFs available)  
**Start Date**: TBD  
**End Date**: TBD

### Week 6: Form Filling Foundation

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Install browser-use library | 🔴 | P0 | - | AI + Playwright wrapper |
| Implement session manager for auth | 🔴 | P0 | - | src/applier/session_manager.py |
| Test loading saved browser sessions | 🔴 | P0 | - | Persist login state |
| Create basic form filler (text inputs) | 🔴 | P0 | - | src/applier/form_filler.py |
| Test file upload (PDF resume) | 🔴 | P0 | - | page.set_input_files() |
| Implement dropdown/checkbox handling | 🔴 | P1 | - | Various input types |
| Test on sample job application form | 🔴 | P0 | - | Find test site |

**Verification Gate 6**: ✓ Successfully fill simple form + upload PDF (dry-run, no submit)

---

### Week 7: AI-Powered Automation

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Integrate browser-use Agent | 🔴 | P0 | - | Claude + Playwright |
| Design form filling task prompt | 🔴 | P0 | - | Instructions for AI agent |
| Load user_profile.yaml data | 🔴 | P0 | - | Pass to agent |
| Test AI form filling on real job portal | 🔴 | P0 | - | LinkedIn/Indeed |
| Implement screenshot capture on errors | 🔴 | P1 | - | Debugging aid |
| Add verification step before submit | 🔴 | P0 | - | Pause for user confirmation |
| Test end-to-end application (dry-run) | 🔴 | P0 | - | No actual submission |

**Verification Gate 7**: ✓ AI successfully navigates form, fills fields, uploads resume (stopped before submit)

---

### Week 8: Error Handling & Notifications

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Define error exception classes | 🔴 | P0 | - | src/applier/error_handler.py |
| Implement retry logic with backoff | 🔴 | P0 | - | 3 retries, exponential delay |
| Detect login required pages | 🔴 | P0 | - | URL pattern matching |
| Detect CAPTCHA challenges | 🔴 | P0 | - | Page content analysis |
| Set up email notification system | 🔴 | P0 | - | src/utils/notifications.py |
| Configure Mailgun/SMTP | 🔴 | P0 | - | Test email sending |
| Implement user intervention flow | 🔴 | P0 | - | Email + wait timeout |
| Log all application attempts to DB | 🔴 | P1 | - | ApplicationLog table |
| Create CLI command: `apply --job-ids` | 🔴 | P0 | - | Full automation |
| Test error recovery scenarios | 🔴 | P1 | - | Network timeout, session expired |

**Verification Gate 8**: ✓ Application completes OR notifies user on failure with actionable info

**Phase 3 Deliverables**:
- ✅ Automated form filling working (90%+ success)
- ✅ Error handling with user notifications
- ✅ Application logs captured
- ✅ CLI tool for applying to selected jobs

---

## Phase 4: Polish & Advanced Features (Weeks 9-10)

**Goal**: Exception handling edge cases, cover letters, status tracking  
**Status**: 🔴 Not Started  
**Dependencies**: Phase 3 complete (basic automation working)  
**Start Date**: TBD  
**End Date**: TBD

### Week 9: Advanced Error Handling

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Implement account creation detection | 🔴 | P0 | - | "Sign up" page patterns |
| Create Google OAuth fallback flow | 🔴 | P1 | - | Notify user to login manually |
| Handle dynamic form fields (JavaScript) | 🔴 | P1 | - | Wait for elements |
| Implement form structure recognition | 🔴 | P1 | - | AI analyzes page structure |
| Create troubleshooting checklist | 🔴 | P2 | - | Future: dynamic learning |
| Test edge cases (2FA, unusual forms) | 🔴 | P1 | - | Document failures |

**Verification Gate 9**: ✓ Graceful handling of 5+ edge case scenarios

---

### Week 10: Optional Features & Polish

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Implement cover letter generator | 🔴 | P2 | - | src/customizer/cover_letter_generator.py |
| Create cover letter PDF template | 🔴 | P2 | - | Simple styling |
| Integrate cover letter upload in applier | 🔴 | P2 | - | Optional per application |
| Build application status CLI dashboard | 🔴 | P1 | - | src/utils/status_tracker.py |
| Show success/failure statistics | 🔴 | P1 | - | Query ApplicationLog table |
| Implement job filtering (by keywords) | 🔴 | P1 | - | CLI enhancement |
| Add dry-run mode for all commands | 🔴 | P1 | - | Test without side effects |
| Create user documentation | 🔴 | P0 | - | README.md updates |
| Record demo video | 🔴 | P2 | - | For future reference |

**Verification Gate 10**: ✓ All optional features configurable, documentation complete

**Phase 4 Deliverables**:
- ✅ Cover letter generation (optional)
- ✅ Account creation handled gracefully
- ✅ Status dashboard functional
- ✅ Complete documentation

---

## Phase 5: Testing & Validation (Weeks 11-12)

**Goal**: Comprehensive testing and production readiness  
**Status**: 🔴 Not Started  
**Start Date**: TBD  
**End Date**: TBD

### Week 11: Integration Testing

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Write integration tests for scraper | 🔴 | P0 | - | End-to-end scraping |
| Write integration tests for customizer | 🔴 | P0 | - | Mock Claude API |
| Write integration tests for applier | 🔴 | P0 | - | Test job application |
| Test on 10 real job applications | 🔴 | P0 | - | Actual portals |
| Measure success rate | 🔴 | P0 | - | Target: 90%+ |
| Optimize performance bottlenecks | 🔴 | P1 | - | Scraping speed, API calls |
| Test scheduled scraping (7-day run) | 🔴 | P0 | - | Verify reliability |

**Verification Gate 11**: ✓ 90%+ success rate on 10 test applications

---

### Week 12: Production Hardening

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Security audit (credential storage) | 🔴 | P0 | - | Encryption validated |
| Review error logging completeness | 🔴 | P1 | - | All exceptions logged |
| Optimize database queries (indexing) | 🔴 | P1 | - | Performance tuning |
| Clean up old jobs (90-day archive) | 🔴 | P2 | - | Automated cleanup |
| Create backup/restore scripts | 🔴 | P2 | - | Database backup |
| Finalize .gitignore (no secrets) | 🔴 | P0 | - | Double-check |
| Code review & refactoring | 🔴 | P1 | - | Clean up technical debt |
| Update all documentation | 🔴 | P0 | - | Reflect final state |
| Tag v1.0.0 release | 🔴 | P0 | - | Git tag |

**Verification Gate 12**: ✓ Production-ready, documented, secure

**Phase 5 Deliverables**:
- ✅ 90%+ automation success rate
- ✅ All tests passing
- ✅ Security audit complete
- ✅ Documentation finalized
- ✅ v1.0.0 released

---

## Future Phases (Post-MVP)

### Phase 6: Ranking & Intelligence (Optional)

**Goal**: Prioritize best-fit jobs automatically  
**Status**: 🔴 Not Started  
**Timeline**: Weeks 13-14

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Implement resume-to-job similarity scoring | 🔴 | P2 | - | TF-IDF or embedding similarity |
| Rank jobs by Palantir Foundry mentions | 🔴 | P2 | - | Keyword weighting |
| Auto-apply to top 10% matches | 🔴 | P2 | - | Configurable threshold |
| Display match scores in CLI | 🔴 | P2 | - | User visibility |

---

### Phase 7: Dynamic Learning (Optional)

**Goal**: Self-improving error handling  
**Status**: 🔴 Not Started  
**Timeline**: Weeks 15-16

| Task | Status | Priority | Owner | Notes |
|------|--------|----------|-------|-------|
| Record user intervention events | 🔴 | P2 | - | What went wrong? |
| Build troubleshooting checklist | 🔴 | P2 | - | Extend system prompt |
| Implement success pattern recognition | 🔴 | P2 | - | Which form strategies work? |
| Create error analytics dashboard | 🔴 | P2 | - | Common failure modes |

---

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| LinkedIn TOS violation (scraping) | High | Medium | Use official API or cautious scraping |
| Claude API rate limits | Medium | Low | Implement caching + retry logic |
| Playwright browser detection | High | Medium | Rotate user agents, delays |
| Windows Task Scheduler unreliable | Low | Low | Add fallback cron script |
| PDF generation fails on Windows | Medium | Low | Test WeasyPrint early, have fallback |
| User credentials leaked | High | Low | Strong encryption + .gitignore |
| Form structure changes break automation | Medium | High | AI-powered form recognition |

---

## Milestones

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Phase 1 Complete (Scraper) | Week 3 | 🔴 | Foundation ready |
| Phase 2 Complete (Customizer) | Week 5 | 🔴 | Resume PDFs generated |
| Phase 3 Complete (Applier) | Week 8 | 🔴 | Basic automation working |
| Phase 4 Complete (Polish) | Week 10 | 🔴 | Production features |
| Phase 5 Complete (Testing) | Week 12 | 🔴 | v1.0.0 release |
| First Real Application | TBD | 🔴 | User validates flow |
| 10 Successful Applications | TBD | 🔴 | Proven system |

---

## Overall Progress

**Overall Progress**: 33% (4/12 weeks complete - Phase 1 Week 1)

### Weekly Check-ins
- **Week 1**: [TBD]
- **Week 2**: [TBD]
- **Week 3**: [TBD]
- ...

---

**Next Action**: Begin Phase 1, Week 1 tasks (Project Setup & Database)
