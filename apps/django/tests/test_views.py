from apps.django.src.calculator import add, subtract  # ✅ Correct path

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 2) == 3
    assert subtract(0, 1) == -1
