'''Test for Operations'''
import pytest
from faker import Faker
from app.plugins.operations import Operations

fake = Faker()

@pytest.fixture
def operations():
    '''Fixture to provide an instance of Operations'''
    return Operations()

@pytest.fixture
def random_numbers():
    '''Fixture to provide random numbers'''
    return fake.random_int(min=1, max=100), fake.random_int(min=1, max=100)

def test_add(operations, random_numbers):
    '''checks addition operation with random numbers'''
    a, b = random_numbers
    result = operations.add(a, b)
    assert result == a + b

def test_subtract(operations, random_numbers):
    '''checks subtraction operation with random numbers'''
    a, b = random_numbers
    result = operations.subtract(a, b)
    assert result == a - b

def test_divide(operations, random_numbers):
    '''Checks division operation with random numbers'''
    a, b = random_numbers
    if b == 0:
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            operations.divide(a, b)
    else:
        result = operations.divide(a, b)
        assert result == a / b

def test_multiply(operations, random_numbers):
    '''checks multiplying operation with random numbers'''
    a, b = random_numbers
    result = operations.multiply(a, b)
    assert result == a * b

# Additional tests for edge cases

def test_operations_add_with_zero(operations):
    '''Test adding zero to a number'''
    assert operations.add(5, 0) == 5
    assert operations.add(0, 0) == 0

def test_operations_subtract_with_zero(operations):
    '''Test subtracting zero from a number'''
    assert operations.subtract(5, 0) == 5
    assert operations.subtract(0, 5) == -5

def test_operations_divide_with_zero(operations):
    '''Test that dividing by zero raises ValueError'''
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        operations.divide(10, 0)

def test_operations_divide_zero_by_number(operations):
    '''Test dividing zero by a number'''
    assert operations.divide(0, 5) == 0

def test_operations_with_negative_numbers(operations):
    '''Test operations with negative numbers'''
    assert operations.add(-5, -10) == -15
    assert operations.subtract(-5, -10) == 5
    assert operations.multiply(-5, -10) == 50
    assert operations.divide(-10, -2) == 5
