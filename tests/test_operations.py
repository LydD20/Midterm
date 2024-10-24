'''Test for Operations'''
import pytest
from faker import Faker
from app.plugins.operations import Operations

fake = Faker()

@pytest.fixture
def operations():
    '''Fixture to provide an instance of Operations'''
    return Operations()  # Fixture provides an instance of Operations

# Parametrize with 5 random pairs of integers (a, b) for testing
@pytest.mark.parametrize("a, b", [(fake.random_int(min=1, max=100), fake.random_int(min=1, max=100)) for _ in range(5)])
def test_add(operations, a, b):
    '''checks addition operation with random numbers'''
    result = operations.add(a, b)
    assert result == a + b

@pytest.mark.parametrize("a, b", [(fake.random_int(min=1, max=100), fake.random_int(min=1, max=100)) for _ in range(5)])
def test_subtract(operations, a, b):
    '''checks subtraction operation with random numbers'''
    result = operations.subtract(a, b)
    assert result == a - b

@pytest.mark.parametrize("a, b", [(fake.random_int(min=1, max=100), fake.random_int(min=1, max=100)) for _ in range(5)])
def test_divide(operations, a, b):
    '''Checks division operation with random numbers'''
    if b == 0:  # To handle division by zero case
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            operations.divide(a, b)
    else:
        result = operations.divide(a, b)
        assert result == a / b

@pytest.mark.parametrize("a, b", [(fake.random_int(min=1, max=100), fake.random_int(min=1, max=100)) for _ in range(5)])
def test_multiply(operations, a, b):
    '''checks multiplying operation with random numbers'''
    result = operations.multiply(a, b)
    assert result == a * b
