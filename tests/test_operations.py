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
