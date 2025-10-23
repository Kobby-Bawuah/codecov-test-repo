"""Tests for Dashboard migrations."""

import importlib.util
import sys
from pathlib import Path


def import_migration_module(module_path):
    """Import a migration module dynamically."""
    spec = importlib.util.spec_from_file_location("migration", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["migration"] = module
    spec.loader.exec_module(module)
    return module


def test_setup_dashboard():
    """Test dashboard setup."""
    base_path = Path(__file__).parent.parent / "migrations" / "0001_initial.py"
    migration = import_migration_module(base_path)
    result = migration.setup_dashboard()
    assert "initialized" in result


def test_teardown_dashboard():
    """Test dashboard teardown."""
    base_path = Path(__file__).parent.parent / "migrations" / "0001_initial.py"
    migration = import_migration_module(base_path)
    result = migration.teardown_dashboard()
    assert "removed" in result


def test_dashboard_version():
    """Test getting dashboard version."""
    base_path = Path(__file__).parent.parent / "migrations" / "0001_initial.py"
    migration = import_migration_module(base_path)
    version = migration.get_dashboard_version()
    assert "v1.0" in version

