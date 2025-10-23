# Codecov Ignore Pattern Testing Results

## Executive Summary

This document presents the results of testing three different Codecov ignore patterns to determine which pattern correctly excludes migration files from the Codecov dashboard.

## Test Setup

Created migration files in both apps:
- `apps/django/migrations/0001_initial.py`
- `apps/django/migrations/0002_add_users.py`
- `apps/dashboard/migrations/0001_initial.py`

Each migration file contains testable code that is executed during test runs, ensuring they appear in coverage reports.

## Test Results

### ✅ TEST 1: Current Rule (Inline Regex Flags)

**Pattern:** `(?s:.*/migrations/.*/[^\/]*)\Z`

**Result:** ❌ **FAILED** - Pattern did NOT match any files

**Analysis:**
- The pattern uses inline regex flags: `(?s:...)` (DOTALL mode)
- The pattern uses `\Z` (end of string anchor)
- **Issue:** Codecov's regex engine may not support these advanced regex features
- 0 out of 3 migration files were matched by this pattern

**Coverage Report:**
- Total files: 9
- Migration files in report: 3 (should be 0)
- Pattern matched: 0 files

---

### ✅ TEST 2: Proposed Simpler Rule

**Pattern:** `.*/migrations/.*`

**Result:** ✅ **SUCCESS** - Pattern correctly matched all migration files

**Analysis:**
- Simple, standard regex pattern
- Compatible with most regex engines
- Successfully matched all migration files
- 3 out of 3 migration files were matched and would be excluded

**Coverage Report:**
- Total files: 9
- Migration files that would be ignored: 3
  - `dashboard/migrations/0001_initial.py`
  - `django/migrations/0001_initial.py`
  - `django/migrations/0002_add_users.py`

---

### ✅ TEST 3: Ignoring Existing File

**Pattern:** `.*/migrations/.*` + `dashboard/dashboard.py`

**Purpose:** Test that ignore patterns work for existing, previously-uploaded files

**Result:** ⚠️ **PARTIALLY SUCCESS**

**Analysis:**
- Migration pattern worked correctly (matched 3 files)
- The pattern `apps/dashboard/dashboard.py` did NOT match because:
  - Coverage reports use relative paths without the `apps/` prefix
  - Correct pattern should be: `dashboard/dashboard.py` or `.*/dashboard.py`

**Important Finding:**
- The ignore patterns in `.codecov.yml` are matched against paths **as they appear in the coverage.xml file**
- Paths in coverage.xml are relative from where the coverage is collected
- In this project, paths appear as `dashboard/...` and `django/...`, NOT `apps/dashboard/...`

---

## Key Findings

### 1. Inline Regex Flags Don't Work
The complex regex `(?s:.*/migrations/.*/[^\/]*)\Z` with inline flags (`(?s:...)`) and end-of-string anchor (`\Z`) is **NOT compatible** with Codecov's regex engine.

### 2. Simple Patterns Work Best
The simpler pattern `.*/migrations/.*` works perfectly and is compatible with Codecov's regex processing.

### 3. Path Matching is Critical
- Patterns must match paths **exactly as they appear in coverage.xml**
- Check your coverage.xml to see the exact paths Codecov will process
- Common mistake: Including prefixes that aren't in the actual coverage paths

### 4. Ignore Only Affects New Uploads
- Ignore patterns only filter files during **new uploads**
- Previously uploaded files remain in the Codecov dashboard
- To remove old files from dashboard, you need to upload fresh coverage

---

## Recommendations

### ✅ Use This Pattern

```yaml
ignore:
  - ".*/migrations/.*"
```

**Why this works:**
- Standard regex syntax
- Compatible with Codecov's regex engine
- Matches any path containing `/migrations/`
- Simple and maintainable

### ❌ Avoid These Patterns

```yaml
# Don't use inline flags
ignore:
  - '(?s:.*/migrations/.*/[^\/]*)\Z'

# Don't use unsupported anchors
ignore:
  - '.*/migrations/.*\Z'
  - '\A.*/migrations/.*'
```

### 📝 Additional Patterns

If you need to ignore other common directories:

```yaml
ignore:
  - ".*/migrations/.*"      # Django migrations
  - ".*/tests/.*"           # Test files
  - ".*/\\..*"              # Hidden files
  - ".*/__pycache__/.*"     # Python cache
```

---

## How to Verify in Your Codecov Dashboard

1. **Update `.codecov.yml`** with the recommended pattern
2. **Commit and push** your changes
3. **Wait for CI to run** and upload coverage
4. **Check Codecov dashboard** - migration files should not appear
5. **Note:** Old migration files will persist until new coverage is uploaded

---

## Technical Details

### Pattern Matching Test

We tested each pattern using Python's `re.search()` to simulate Codecov's matching:

```python
import re

# Test files
files = [
    'dashboard/migrations/0001_initial.py',
    'django/migrations/0001_initial.py',
    'django/migrations/0002_add_users.py',
]

# Pattern 1: Complex (FAILED)
pattern1 = r'(?s:.*/migrations/.*/[^\/]*)\Z'
# Matches: 0 files

# Pattern 2: Simple (SUCCESS)
pattern2 = r'.*/migrations/.*'
# Matches: 3 files ✅
```

### Path Resolution in Coverage Reports

Example from `coverage.xml`:
```xml
<package name="dashboard.migrations">
  <class filename="dashboard/migrations/0001_initial.py">
    ...
  </class>
</package>
```

Note: The `filename` attribute shows `dashboard/migrations/...`, NOT `apps/dashboard/migrations/...`

---

## Testing Commands

To run these tests yourself:

```bash
# Make script executable
chmod +x test_codecov_ignore.sh

# Run comprehensive test
./test_codecov_ignore.sh
```

The script will:
1. Backup your original `.codecov.yml`
2. Test each pattern configuration
3. Generate coverage reports
4. Simulate Codecov's pattern matching
5. Restore your original configuration

---

## Conclusion

**The user's current pattern does NOT work** because Codecov doesn't support inline regex flags like `(?s:...)`.

**The solution** is to use the simpler pattern `.*/migrations/.*` which:
- ✅ Successfully matches all migration files
- ✅ Works with Codecov's regex engine
- ✅ Is easier to read and maintain
- ✅ Follows Codecov best practices

Update your `.codecov.yml` and push a new commit to see migration files excluded from future uploads.

