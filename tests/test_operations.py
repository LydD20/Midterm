import pytest
from app.plugins.operations import Operations

@pytest.fixture
def operations():
    '''Fixture to provide an instance of Operations'''
    return Operations()  # Fixture provides an instance of Operations

def test_add(operations, a, b):
    '''checks addition operation'''
    result = operations.add(a, b)  # Call the method with a and b
    assert result == a + b

def test_subtract(operations, a, b):
    '''checks subtraction operation'''
    result = operations.subtract(a, b)  # Call the method with a and b
    assert result == a - b

def test_divide(operations, a, b):
    '''Checks division operation'''
    if b == 0:
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            operations.divide(a, b)
    else:
        result = operations.divide(a, b)
        assert result == a / b

def test_multiply(operations, a, b):
    '''checks multiplying operation'''
    result = operations.multiply(a, b)  # Call the method with a and b
    assert result == a * b
