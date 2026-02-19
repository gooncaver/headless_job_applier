# Headless Job Applier - Bug Tracking & Fixes

**Version**: 1.0.0  
**Last Updated**: February 19, 2026  
**Purpose**: Document bugs, their resolutions, and lessons learned

---

## Active Bugs

### Critical (P0)
_No active critical bugs._

---

### High Priority (P1)
_No active high-priority bugs._

---

### Medium Priority (P2)
_No active medium-priority bugs._

---

### Low Priority (P3)
_No active low-priority bugs._

---

## Resolved Bugs

### BUG-2026-02-19-001: SQLAlchemy 2.0 Reserved Keyword Conflict

**Bug ID**: BUG-2026-02-19-001  
**Title**: SQLAlchemy 2.0 raises InvalidRequestError for 'metadata' column name  
**Severity**: Critical  
**Component**: Database  
**Reported Date**: 2026-02-19  
**Resolved Date**: 2026-02-19  
**Reported By**: Test execution  
**Assigned To**: Development team

**Description**:
When running the Phase 1 verification script, imports fail with:
```
InvalidRequestError: Attribute name 'metadata' is reserved when using the Declarative API
```

The ApplicationLog model had a column named `metadata`, which is reserved in SQLAlchemy 2.0.

**Environment**:
- OS: Windows 11
- Python Version: 3.13.1
- SQLAlchemy Version: 2.0.33

**Reproduction Steps**:
1. Run `python verify_phase1.py`
2. Observe import error when loading database models

**Root Cause**:
SQLAlchemy 2.0.x made `metadata` a reserved attribute name for the Declarative base. Any column named `metadata` conflicts with the model's internal `__table__.metadata` attribute.

**Fix**:
Renamed the column from `metadata` to `event_metadata` in:
- `src/database/models.py` (ApplicationLog.event_metadata)
- `src/database/engine.py` (db_manager.get_stats() import)
- `tests/test_database.py` (test_log_event_factory)
- Updated `ApplicationLog.log_event()` factory method signature

**Verification**:
- ✅ All imports successful
- ✅ Database models instantiate correctly
- ✅ 13/13 unit tests passing
- ✅ Phase 1 verification 5/5 checks passing

**Lessons Learned**:
- SQLAlchemy 2.0 introduced breaking changes around reserved attribute names
- Reserved keywords: metadata, mapper, registry, logger, etc.
- Always reference SQLAlchemy 2.0 migration guide when upgrading from 1.x
- Testing imports early catches these issues before full integration

**Related Issues**:
- SQLAlchemy 2.0 Migration Guide: https://docs.sqlalchemy.org/en/20/changelog/migration_20.html

---

### BUG-2026-02-19-002: SQLAlchemy 2.0 Raw SQL Execution Error

**Bug ID**: BUG-2026-02-19-002  
**Title**: SQLAlchemy 2.0 rejects raw SQL strings in connection.execute()  
**Severity**: Critical  
**Component**: Database  
**Reported Date**: 2026-02-19  
**Resolved Date**: 2026-02-19  
**Reported By**: Health check test  
**Assigned To**: Development team

**Description**:
Database health check fails with:
```
StatementError: (builtins.TypeError) Not an executable object: 'SELECT 1'
```

The `health_check()` method was passing raw SQL string to connection.execute().

**Environment**:
- OS: Windows 11
- Python Version: 3.13.1
- SQLAlchemy Version: 2.0.33

**Reproduction Steps**:
1. Run `python src/main.py status`
2. Database health check fails

**Root Cause**:
SQLAlchemy 2.0 removed support for passing raw SQL strings directly to `execute()`. All raw SQL must be wrapped in `text()` constructor.

**Fix**:
- Added `text` import: `from sqlalchemy import text`
- Wrapped raw SQL: `connection.execute(text("SELECT 1"))`
- File: `src/database/engine.py` (lines 3, 95)

**Verification**:
- ✅ Health check executes successfully
- ✅ Database statistics query works
- ✅ Status command displays correct output

**Lessons Learned**:
- SQLAlchemy 2.0 enforces type safety on SQL execution
- Always use `text()` for raw SQL in 2.0+
- Use ORM queries (db.query()) instead of raw SQL when possible
- Better IDE autocomplete and error detection with typed SQL

**Related Issues**:
- SQLAlchemy 2.0 text() documentation: https://docs.sqlalchemy.org/en/20/core/text.html

---

### BUG-2026-02-19-003: Import Path Resolution Conflicts

**Bug ID**: BUG-2026-02-19-003  
**Title**: Mixed absolute/relative imports cause ModuleNotFoundError  
**Severity**: High  
**Component**: CLI, Database  
**Reported Date**: 2026-02-19  
**Resolved Date**: 2026-02-19  
**Reported By**: CLI execution  
**Assigned To**: Development team

**Description**:
Running CLI command fails with:
```
ImportError: cannot import name 'init_db' from 'src.database.engine'
ModuleNotFoundError: No module named 'database.engine'
```

The project had inconsistent import paths:
- `src/main.py` used `from src.database.engine import ...`
- `src/database/__init__.py` used both absolute and relative imports
- This caused failures in different execution contexts (CLI vs verification script)

**Environment**:
- OS: Windows 11
- Python Version: 3.13.1
- VS Code workspace

**Reproduction Steps**:
1. Run `python src/main.py status`
2. Import fails with ModuleNotFoundError
3. Run `python verify_phase1.py`
4. Different import error than CLI

**Root Cause**:
Mixed import strategies:
1. `src/main.py` adds `src` to sys.path then uses `from src.database...` (absolute)
2. `src/database/engine.py` used `from src.database.models...` (absolute)
3. But when `src/` is in sys.path, `src.database` doesn't exist as a module

**Fix**:
Standardized on relative imports throughout the project:
- `src/main.py`: Changed to `from database.engine import ...` (after src added to path)
- `src/database/engine.py`: Changed to `from .models import Base` (relative)
- `src/database/__init__.py`: Changed to `from .models import ...` (relative)
- `src/__init__.py`: Removed problematic cross-module imports

**Verification**:
- ✅ CLI commands execute successfully
- ✅ Verification script runs without import errors
- ✅ All module imports resolve correctly
- ✅ Both relative and absolute import contexts work

**Lessons Learned**:
- Python import resolution is path-dependent
- Relative imports work in any context (package vs standalone)
- Absolute imports from `src.` only work when project root is in sys.path
- Best practice: Use relative imports within packages, add explicit path only when necessary
- Test imports from both CLI and test script perspectives

**Related Issues**:
- Python import documentation: https://docs.python.org/3/reference/import_system.html

---

### BUG-2026-02-19-004: Missing init_db() Function

**Bug ID**: BUG-2026-02-19-004  
**Title**: CLI command 'init-db-cmd' calls non-existent init_db() function  
**Severity**: High  
**Component**: CLI  
**Reported Date**: 2026-02-19  
**Resolved Date**: 2026-02-19  
**Reported By**: Test execution  
**Assigned To**: Development team

**Description**:
CLI init-db-cmd fails with:
```
ImportError: cannot import name 'init_db' from 'src.database.engine'
```

The `src/main.py` imports and calls a non-existent `init_db()` function. The actual method is `DatabaseManager.create_all_tables()`.

**Root Cause**:
Incomplete refactoring. The database engine was designed with `create_all_tables()` method on DatabaseManager, but the CLI still referenced the old `init_db()` function.

**Fix**:
- Removed `init_db` from imports in `src/main.py` line 11
- Replaced all calls to `init_db()` with `db_manager.create_all_tables()`
- Updated 3 locations: setup(), init_db_cmd(), reset_db_cmd() functions
- File: `src/main.py` (lines 29, 106, 145)

**Verification**:
- ✅ `python src/main.py init-db-cmd` executes successfully
- ✅ Database file created: `database/jobs.db`
- ✅ Tables created: jobs, applications, application_logs
- ✅ Health check passes

**Lessons Learned**:
- Keep imports and their usage in sync during refactoring
- Search for all usages before removing a function
- Test affected code paths after refactoring
- Consider using linters to catch unused imports

**Related Issues**:
- None

---

### BUG-2026-02-19-005: Python 3.13.1 Package Compatibility

**Bug ID**: BUG-2026-02-19-005  
**Title**: Multiple packages fail to install on Python 3.13.1  
**Severity**: Critical  
**Component**: Dependency Management  
**Reported Date**: 2026-02-19  
**Resolved Date**: 2026-02-19  
**Reported By**: pip installation  
**Assigned To**: Development team

**Description**:
Installing requirements.txt fails with multiple errors:
```
ERROR: error: linker 'link.exe' not found
ERROR: error: 'build_ext' object has no attribute 'cython_sources'
ERROR: Could not find a version that satisfies pydantic-core==2.18.4
```

Packages with compilation requirements (pydantic-core, PyYAML) lack Python 3.13 wheels.

**Environment**:
- OS: Windows 11
- Python Version: 3.13.1
- Visual Studio 2022 (C++ build tools NOT in PATH)

**Issues**:
1. **pydantic-core**: Versions < 2.9.2 have no Python 3.13 wheels; pip backtracked through 20+ versions
2. **PyYAML**: Version 6.0 requires C compilation; no wheels for Python 3.13
3. **anthropic**: Version 0.25.10 doesn't exist (jumped to 0.26.0)
4. **crewai**: Version 0.50.0 doesn't exist (jumped 0.203.2 → 1.0.0)

**Root Cause**:
Python 3.13 released in October 2023; many packages haven't published wheels yet. Compilation requires Rust (pydantic-core) or C/C++ (PyYAML), with proper PATH setup.

**Fix Strategy**:
1. **Upgrade pydantic early**: Pre-install pydantic==2.9.2 (has wheels) before openai to prevent backtracking
2. **Replace PyYAML**: Use ruamel.yaml==0.18.6 (has Python 3.13 wheels)
3. **Remove problematic packages**: 
   - anthropic (use openai instead)
   - crewai (defer to Phase 2 Week 3 after scraper foundation)
   - weasyprint (defer to Phase 2 Week 5)
4. **Explicit versions**: Pin to versions with confirmed Python 3.13 wheels

**Applied Changes**:
- Updated requirements.txt to Phase 1 minimal dependencies (31 packages, all with wheels)
- Pre-install pydantic==2.9.2 before openai==1.10.0
- Use ruamel.yaml==0.18.6 instead of PyYAML
- Updated config.yaml and documentation for OpenAI (GPT-4o)

**Verification**:
- ✅ 40+ packages installed successfully via venv pip
- ✅ All packages use pre-built wheels (no compilation)
- ✅ Installation time < 2 minutes
- ✅ No C++ compiler warnings or errors
- ✅ All imports resolve correctly

**Lessons Learned**:
- New Python versions take time for package ecosystem to mature
- Always check wheel availability before pinning versions
- Pre-installing packages with dependency conflicts can prevent pip backtracking
- Use pre-built wheels to avoid compilation dependencies
- Test on development Python version early
- Phase-based requirements help manage compatibility issues
- Fallback LLM provider (OpenAI) instead of single provider dependency

**Workarounds**:
- Install Visual Studio 2022 C++ Build Tools (if needed for future packages)
- Downgrade to Python 3.12 (has wider wheel support) if issues persist
- Use conda instead of pip (often has better wheel availability)
- Monitor package release schedules for Python 3.13 wheel additions

**Related Issues**:
- Python 3.13 Release: https://www.python.org/downloads/release/python-3130/
- pydantic v2 Windows Installation: https://docs.pydantic.dev/latest/

---

### Template Entry

**Bug ID**: BUG-YYYY-MM-DD-001  
**Title**: [Short description]  
**Severity**: Critical | High | Medium | Low  
**Component**: Scraper | Customizer | Applier | Database | CLI  
**Reported Date**: YYYY-MM-DD  
**Resolved Date**: YYYY-MM-DD  
**Reported By**: [Name or system]  
**Assigned To**: [Developer name]

**Description**:
Detailed description of the bug, including:
- What was expected
- What actually happened
- Steps to reproduce

**Environment**:
- OS: Windows 11
- Python Version: 3.11.x
- Playwright Version: 1.45.x
- CrewAI Version: 0.50.x

**Reproduction Steps**:
1. Step 1
2. Step 2
3. Step 3

**Root Cause**:
Explanation of why the bug occurred.

**Fix**:
Description of the fix applied, including:
- Code changes
- Configuration updates
- Dependencies updated

**Verification**:
How the fix was verified:
- Test cases
- Manual testing
- Regression testing

**Lessons Learned**:
What we learned from this bug to prevent similar issues.

**Related Issues**:
- Links to related bugs or feature requests

---

## Bug Statistics

| Metric | Count |
|--------|-------|
| Total Bugs Reported | 5 |
| Resolved | 5 |
| Open (Critical) | 0 |
| Open (High) | 0 |
| Open (Medium) | 0 |
| Open (Low) | 0 |
| Average Resolution Time | < 1 hour |
| Phase 1 Week 1 Bugs | 5 (all resolved) |

---

## Known Issues & Workarounds

### Issue: LinkedIn Scraping Rate Limiting

**Description**: LinkedIn may block IP after excessive scraping requests.

**Workaround**:
- Limit scraping to 1 request per 3 seconds
- Use residential proxy if blocked
- Consider LinkedIn API (paid) for production

**Status**: Not a bug, expected behavior

---

### Issue: WeasyPrint Font Rendering on Windows

**Description**: WeasyPrint may not render certain fonts correctly on Windows.

**Workaround**:
- Use standard web-safe fonts (Arial, Times New Roman)
- Install GTK+ for Windows for better font support
- Test PDF output early in development

**Status**: Known limitation, documented

---

### Issue: Playwright Chromium Detection

**Description**: Some job portals detect Playwright's headless browser as a bot.

**Workaround**:
- Use `slow_motion_ms` to simulate human behavior
- Randomize mouse movements
- Use `headed` mode for debugging
- Set realistic viewport size

**Status**: Ongoing research, mitigation in place

---

## Bug Triage Process

### Severity Definitions

**Critical (P0)**:
- System crashes or data loss
- Security vulnerabilities
- Complete feature failure (scraper not working at all)
- Resolution Time: <24 hours

**High Priority (P1)**:
- Major feature degradation (e.g., 50%+ application failures)
- Incorrect data in database
- Email notifications not sent
- Resolution Time: <3 days

**Medium Priority (P2)**:
- Minor feature issues (e.g., cover letter formatting)
- UI/UX improvements
- Performance issues (not critical)
- Resolution Time: <1 week

**Low Priority (P3)**:
- Cosmetic issues
- Documentation updates
- Nice-to-have features
- Resolution Time: <2 weeks or backlog

---

## Reporting a Bug

To report a bug, add an entry above using this template:

```markdown
**Bug ID**: BUG-2026-02-18-001
**Title**: Scraper fails on LinkedIn job search
**Severity**: High
**Component**: Scraper
**Reported Date**: 2026-02-18
**Resolved Date**: [TBD]
**Reported By**: User

**Description**:
When running `python src/main.py scrape`, the LinkedIn scraper times out after 30 seconds without retrieving any jobs.

**Environment**:
- OS: Windows 11
- Python Version: 3.11.5
- Playwright Version: 1.45.0

**Reproduction Steps**:
1. Configure config.yaml with LinkedIn credentials
2. Run `python src/main.py scrape`
3. Observe timeout error in logs

**Root Cause**:
[To be investigated]

**Fix**:
[TBD]
```

---

## Testing Checklist (Post-Fix)

After fixing any bug, verify:

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing confirms fix
- [ ] No regression in related features
- [ ] Documentation updated
- [ ] Changelog entry added
- [ ] Code reviewed (if applicable)

---

## Common Error Patterns

### Playwright Errors

**TimeoutError: Waiting for selector timeout**
- **Cause**: Element not found or page load slow
- **Fix**: Increase timeout, add wait conditions, check selector accuracy

**Error: Browser disconnected**
- **Cause**: Chromium crashed or network issue
- **Fix**: Add retry logic, check system resources

---

### Claude API Errors

**Rate Limit Exceeded**
- **Cause**: Too many requests in short time
- **Fix**: Implement exponential backoff, cache responses

**Invalid API Key**
- **Cause**: Missing or incorrect ANTHROPIC_API_KEY
- **Fix**: Verify .env file, check environment variables

---

### Database Errors

**IntegrityError: UNIQUE constraint failed**
- **Cause**: Attempting to insert duplicate job
- **Fix**: Check deduplication logic, handle exception gracefully

**OperationalError: database is locked**
- **Cause**: Multiple processes accessing SQLite simultaneously
- **Fix**: Use connection pooling, add retry logic

---

## Debugging Tips

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Playwright Debugging
```python
# Run in headed mode to see browser
browser = playwright.chromium.launch(headless=False, slow_mo=1000)

# Take screenshots on failure
page.screenshot(path="debug_screenshot.png")

# Enable Playwright debug logs
PWDEBUG=1 python src/main.py scrape
```

### Database Inspection
```bash
# Open SQLite database
sqlite3 database/jobs.db

# View tables
.tables

# Query jobs
SELECT * FROM jobs LIMIT 10;
```

---

## Change Log Integration

When a bug is fixed, update [changelog.md](changelog.md) with:
- Bug ID
- Fix description
- Version number

---

**Next Steps**: 
1. Monitor for bugs during Phase 1 implementation
2. Update this document as issues arise
3. Maintain bug statistics for quality tracking
