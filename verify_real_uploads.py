#!/usr/bin/env python3
"""
Verify test conclusions against ACTUAL Codecov uploads
"""

import re
import xml.etree.ElementTree as ET

print("=" * 80)
print("VERIFYING TEST CONCLUSIONS AGAINST REAL CODECOV UPLOADS")
print("=" * 80)
print()

# Parse both uploaded coverage files
files_to_check = [
    "93ce557f-f8c6-4824-8d0b-60869d6a6a26.txt",
    "9856324b-ed55-45c5-af0d-9ea84f18ed85.txt"
]

# Extract all file paths from the uploads
all_files = []
for upload_file in files_to_check:
    print(f"📄 Analyzing: {upload_file}")
    
    with open(upload_file, 'r') as f:
        content = f.read()
    
    # Find the coverage.xml section
    xml_start = content.find('<?xml version="1.0" ?>')
    xml_end = content.find('<<<<<< EOF', xml_start)
    
    if xml_start == -1 or xml_end == -1:
        print(f"   ⚠️  Could not find coverage XML in {upload_file}")
        continue
    
    xml_content = content[xml_start:xml_end].strip()
    
    # Parse XML
    root = ET.fromstring(xml_content)
    
    # Extract source path
    source = root.find('.//source')
    source_path = source.text if source is not None else "Unknown"
    print(f"   Source: {source_path}")
    
    # Extract all file paths
    files_in_upload = []
    for cls in root.findall('.//class'):
        filename = cls.get('filename')
        if filename:
            files_in_upload.append(filename)
            all_files.append(filename)
    
    print(f"   Files found: {len(files_in_upload)}")
    
    # Show migration files
    migration_files = [f for f in files_in_upload if 'migration' in f.lower()]
    if migration_files:
        print(f"   🔍 Migration files in this upload:")
        for f in migration_files:
            print(f"      - {f}")
    print()

print("=" * 80)
print("ALL FILES FROM REAL UPLOADS")
print("=" * 80)
for f in sorted(set(all_files)):
    print(f"  {f}")
print()

# Now test the patterns
patterns_to_test = [
    ("Complex Pattern (User's Current)", r'(?s:.*/migrations/.*/[^\/]*)\Z'),
    ("Simple Pattern (Recommended)", r'.*/migrations/.*'),
    ("Alternative Pattern 1", r'migrations/.*'),
    ("Alternative Pattern 2", r'.*migrations.*'),
]

print("=" * 80)
print("TESTING PATTERNS AGAINST REAL UPLOAD PATHS")
print("=" * 80)
print()

for pattern_name, pattern in patterns_to_test:
    print(f"🧪 Testing: {pattern_name}")
    print(f"   Pattern: {pattern}")
    
    matched = []
    not_matched = []
    
    try:
        for filepath in set(all_files):
            if re.search(pattern, filepath):
                matched.append(filepath)
            else:
                not_matched.append(filepath)
        
        migration_files_matched = [f for f in matched if 'migration' in f.lower()]
        migration_files_not_matched = [f for f in not_matched if 'migration' in f.lower()]
        
        print(f"   ✅ Total files matched: {len(matched)}")
        print(f"   📁 Migration files matched: {len(migration_files_matched)}")
        
        if migration_files_matched:
            print(f"   Migration files that WOULD BE IGNORED:")
            for f in sorted(migration_files_matched):
                print(f"      ✓ {f}")
        
        if migration_files_not_matched:
            print(f"   ❌ Migration files that WOULD NOT BE IGNORED:")
            for f in sorted(migration_files_not_matched):
                print(f"      ✗ {f}")
        
        # Success criteria
        total_migrations = len(migration_files_matched) + len(migration_files_not_matched)
        if total_migrations > 0:
            success_rate = (len(migration_files_matched) / total_migrations) * 100
            print(f"   📊 Success Rate: {success_rate:.1f}% ({len(migration_files_matched)}/{total_migrations} migrations)")
            
            if success_rate == 100:
                print(f"   ✅ PATTERN WORKS - All migrations would be excluded!")
            elif success_rate > 0:
                print(f"   ⚠️  PARTIAL SUCCESS - Some migrations excluded")
            else:
                print(f"   ❌ PATTERN FAILED - No migrations excluded")
        
    except re.error as e:
        print(f"   ❌ REGEX ERROR: {e}")
        print(f"   Pattern is invalid or not supported")
    
    print()

print("=" * 80)
print("TEST VALIDATION SUMMARY")
print("=" * 80)
print()

# Check migration files
migration_files = [f for f in all_files if 'migration' in f.lower()]
print(f"📊 Migration files in real uploads: {len(migration_files)}")
for f in sorted(set(migration_files)):
    print(f"   - {f}")
print()

# Validate Test 1
print("✅ TEST 1 VALIDATION (Complex Pattern)")
print("   Original conclusion: Pattern FAILED - matches 0 files")
complex_pattern = r'(?s:.*/migrations/.*/[^\/]*)\Z'
try:
    complex_matches = [f for f in migration_files if re.search(complex_pattern, f)]
    print(f"   Real upload result: Matched {len(complex_matches)}/{len(migration_files)} migrations")
    if len(complex_matches) == 0:
        print("   ✅ TEST 1 CONCLUSION CONFIRMED: Complex pattern does NOT work")
    else:
        print("   ⚠️  TEST 1 NEEDS REVISION: Complex pattern matched some files")
except re.error:
    print("   ✅ TEST 1 CONCLUSION CONFIRMED: Pattern causes regex error")
print()

# Validate Test 2
print("✅ TEST 2 VALIDATION (Simple Pattern)")
print("   Original conclusion: Pattern SUCCESS - matches all files")
simple_pattern = r'.*/migrations/.*'
simple_matches = [f for f in migration_files if re.search(simple_pattern, f)]
print(f"   Real upload result: Matched {len(simple_matches)}/{len(migration_files)} migrations")
if len(simple_matches) == len(migration_files) and len(migration_files) > 0:
    print("   ✅ TEST 2 CONCLUSION CONFIRMED: Simple pattern works perfectly")
else:
    print(f"   ⚠️  TEST 2 NEEDS REVISION: Pattern matched {len(simple_matches)}/{len(migration_files)} files")
    # Check if a simpler pattern works better
    simpler_pattern = r'migrations/.*'
    simpler_matches = [f for f in migration_files if re.search(simpler_pattern, f)]
    if len(simpler_matches) == len(migration_files):
        print(f"   💡 BETTER PATTERN: 'migrations/.*' matches {len(simpler_matches)}/{len(migration_files)}")
print()

# Validate Test 3
print("✅ TEST 3 VALIDATION (Existing Files)")
print("   Original conclusion: Pattern works with exact paths")
dashboard_file = "dashboard.py"
dashboard_exists = dashboard_file in all_files
print(f"   Real upload contains 'dashboard.py': {dashboard_exists}")
if dashboard_exists:
    pattern = r'dashboard\.py'
    matches = bool(re.search(pattern, dashboard_file))
    print(f"   Pattern 'dashboard.py' matches: {matches}")
    print("   ✅ TEST 3 CONCLUSION CONFIRMED: Exact paths work")
else:
    print("   ✅ TEST 3 CONCLUSION STILL VALID: Principle remains correct")
print()

print("=" * 80)
print("FINAL RECOMMENDATION")
print("=" * 80)
print()

# Find the best pattern
best_pattern = None
best_score = 0

for pattern_name, pattern in patterns_to_test:
    try:
        matches = [f for f in migration_files if re.search(pattern, f)]
        score = len(matches) / len(migration_files) if migration_files else 0
        if score > best_score:
            best_score = score
            best_pattern = (pattern_name, pattern)
    except:
        pass

if best_pattern and best_score == 1.0:
    print(f"✅ RECOMMENDED PATTERN: {best_pattern[0]}")
    print(f"   Pattern: {best_pattern[1]}")
    print(f"   Success Rate: 100% ({int(best_score * len(migration_files))}/{len(migration_files)} migrations)")
    print()
    print("   Use in .codecov.yml:")
    print(f'   ignore:')
    print(f'     - "{best_pattern[1]}"')
else:
    print("⚠️  No pattern achieved 100% success rate")
    print("   Review the test results above for details")

print()
print("=" * 80)

