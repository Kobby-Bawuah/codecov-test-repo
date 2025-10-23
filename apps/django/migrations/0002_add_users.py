"""Add users table migration."""

def apply_migration():
    """Apply the users migration."""
    print("Applying users migration...")
    return True

def reverse_migration():
    """Reverse the users migration."""
    print("Reversing users migration...")
    return True

def create_user_table():
    """Create user table."""
    return "CREATE TABLE users (id INT, name VARCHAR(100))"

