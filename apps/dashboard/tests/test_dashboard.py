from apps.dashboard.dashboard import dashboard_function, get_welcome_message  # ✅ Ensure correct path

def test_dashboard_function():
    assert dashboard_function() == 'Dashboard Page'

def test_get_welcome_message():
    assert get_welcome_message('Alice') == 'Welcome to the dashboard, Alice!'
    assert get_welcome_message('Bob') == 'Welcome to the dashboard, Bob!'
