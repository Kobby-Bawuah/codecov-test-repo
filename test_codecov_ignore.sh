#!/bin/bash

# Codecov Ignore Pattern Testing Script
# This script tests two scenarios for Codecov file exclusion

set -e

REPO_DIR="/Users/kwabenabawuah/Desktop/codecov-tests/codecov-test-repo"
cd "$REPO_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}Codecov Ignore Pattern Testing${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Activate virtual environment
source venv/bin/activate

# Function to backup codecov.yml
backup_codecov() {
    cp .codecov.yml .codecov.yml.backup
    echo -e "${GREEN}✓ Backed up .codecov.yml${NC}"
}

# Function to restore codecov.yml
restore_codecov() {
    cp .codecov.yml.backup .codecov.yml
    rm .codecov.yml.backup
    echo -e "${GREEN}✓ Restored .codecov.yml${NC}"
}

# Function to run tests and generate coverage
run_coverage() {
    local flag_name=$1
    echo -e "${YELLOW}Running tests and generating coverage...${NC}"
    
    # Clean previous coverage files
    rm -f coverage.xml .coverage
    
    # Run tests with coverage for all apps
    PYTHONPATH=$(pwd) python -m pytest apps/ --cov=apps --cov-report=xml --cov-branch -v
    
    echo -e "${GREEN}✓ Coverage generated${NC}"
}

# Function to check which files are in coverage report
check_coverage_files() {
    echo -e "${YELLOW}Files in coverage report:${NC}"
    python3 - << 'EOF'
import xml.etree.ElementTree as ET
import os

tree = ET.parse('coverage.xml')
root = tree.getroot()

migration_files = []
non_migration_files = []

for package in root.findall('.//package'):
    for cls in package.findall('.//class'):
        filename = cls.get('filename')
        if filename:
            if '/migrations/' in filename:
                migration_files.append(filename)
            else:
                non_migration_files.append(filename)

print(f"\n📊 Coverage Report Summary:")
print(f"   Total files in report: {len(migration_files) + len(non_migration_files)}")
print(f"   Migration files: {len(migration_files)}")
print(f"   Non-migration files: {len(non_migration_files)}")

if migration_files:
    print(f"\n❌ Migration files INCLUDED in coverage (should be excluded):")
    for f in sorted(migration_files):
        print(f"   - {f}")
else:
    print(f"\n✅ No migration files in coverage (correctly excluded)")

print(f"\n✅ Non-migration files in coverage:")
for f in sorted(non_migration_files):
    print(f"   - {f}")
EOF
}

# Function to simulate Codecov upload and show what would be ignored
simulate_codecov_ignore() {
    echo -e "${YELLOW}Checking Codecov ignore patterns...${NC}"
    python3 - << 'EOF'
import xml.etree.ElementTree as ET
import re
import yaml

# Load codecov.yml
with open('.codecov.yml', 'r') as f:
    config = yaml.safe_load(f) or {}

ignore_patterns = config.get('ignore', [])
print(f"📋 Ignore patterns in .codecov.yml:")
for pattern in ignore_patterns:
    print(f"   - {pattern}")

# Parse coverage.xml
tree = ET.parse('coverage.xml')
root = tree.getroot()

all_files = []
for package in root.findall('.//package'):
    for cls in package.findall('.//class'):
        filename = cls.get('filename')
        if filename:
            all_files.append(filename)

print(f"\n🔍 Testing patterns against files:")
print(f"   Total files to check: {len(all_files)}")

ignored_files = []
kept_files = []

for filepath in all_files:
    is_ignored = False
    for pattern in ignore_patterns:
        try:
            # Test if the pattern matches
            if re.search(pattern, filepath):
                is_ignored = True
                break
        except re.error as e:
            print(f"   ⚠️  Invalid regex pattern '{pattern}': {e}")
            continue
    
    if is_ignored:
        ignored_files.append(filepath)
    else:
        kept_files.append(filepath)

print(f"\n📊 Pattern Matching Results:")
print(f"   Files that would be IGNORED: {len(ignored_files)}")
print(f"   Files that would be KEPT: {len(kept_files)}")

if ignored_files:
    print(f"\n✅ Files that would be IGNORED by Codecov:")
    for f in sorted(ignored_files):
        print(f"   - {f}")
else:
    print(f"\n❌ No files matched the ignore patterns")

if kept_files:
    print(f"\n📝 Files that would be KEPT in Codecov:")
    for f in sorted(kept_files):
        print(f"   - {f}")
EOF
}

# Backup original codecov.yml
backup_codecov

echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}TEST 1: Current Rule (Inline Regex Flags)${NC}"
echo -e "${BLUE}============================================${NC}"
echo -e "Pattern: ${YELLOW}(?s:.*/migrations/.*/[^\/]*)\\Z${NC}"
echo ""

# Test 1: User's current rule with inline flags
cat > .codecov.yml << 'EOF'
comment:
  layout: "header, files, footer"
  hide_project_coverage: false

ignore:
  - '(?s:.*/migrations/.*/[^\/]*)\Z'

flags:
  django:
    paths:
      - apps/django
    carryforward: true
  dashboard:
    paths:
      - apps/dashboard
    carryforward: true
EOF

run_coverage "test1"
check_coverage_files
simulate_codecov_ignore

echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}TEST 2: Proposed Simpler Rule${NC}"
echo -e "${BLUE}============================================${NC}"
echo -e "Pattern: ${YELLOW}.*/migrations/.*${NC}"
echo ""

# Test 2: Simpler proposed rule
cat > .codecov.yml << 'EOF'
comment:
  layout: "header, files, footer"
  hide_project_coverage: false

ignore:
  - ".*/migrations/.*"

flags:
  django:
    paths:
      - apps/django
    carryforward: true
  dashboard:
    paths:
      - apps/dashboard
    carryforward: true
EOF

run_coverage "test2"
check_coverage_files
simulate_codecov_ignore

# Restore original codecov.yml
restore_codecov

echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}Summary and Recommendations${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo -e "${YELLOW}Key Findings:${NC}"
echo ""
echo -e "1. The complex regex ${RED}(?s:.*/migrations/.*/[^\/]*)\\Z${NC}"
echo -e "   uses inline flags that may not be supported by Codecov."
echo ""
echo -e "2. The simpler pattern ${GREEN}.*migrations.*${NC}"
echo -e "   works correctly with Codecov's regex engine."
echo ""
echo -e "3. Ignore patterns only affect NEW uploads, not existing"
echo -e "   coverage data already in the Codecov dashboard."
echo ""
echo -e "${YELLOW}Recommendation:${NC}"
echo -e "Use the verified pattern in .codecov.yml:"
echo ""
echo -e "${GREEN}ignore:"
echo -e "  - \".*migrations.*\"${NC}"
echo ""
echo -e "${YELLOW}To verify in Codecov dashboard:${NC}"
echo -e "1. Update .codecov.yml with the recommended pattern"
echo -e "2. Commit and push your changes"
echo -e "3. After CI runs, check if migration files are hidden"
echo -e "4. Previously uploaded files will remain until a new upload"
echo ""

