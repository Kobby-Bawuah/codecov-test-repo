"""Tests for Django migrations."""

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


def test_initial_migration_apply():
    """Test applying initial migration."""
    base_path = Path(__file__).parent.parent / "migrations" / "0001_initial.py"
    migration = import_migration_module(base_path)
    assert migration.apply_migration() is True


def test_initial_migration_reverse():
    """Test reversing initial migration."""
    base_path = Path(__file__).parent.parent / "migrations" / "0001_initial.py"
    migration = import_migration_module(base_path)
    assert migration.reverse_migration() is True


def test_migration_status():
    """Test getting migration status."""
    base_path = Path(__file__).parent.parent / "migrations" / "0001_initial.py"
    migration = import_migration_module(base_path)
    status = migration.get_migration_status()
    assert "0001_initial" in status


def test_create_user_table():
    """Test user table creation."""
    base_path = Path(__file__).parent.parent / "migrations" / "0002_add_users.py"
    migration = import_migration_module(base_path)
    sql = migration.create_user_table()
    assert "CREATE TABLE users" in sql

