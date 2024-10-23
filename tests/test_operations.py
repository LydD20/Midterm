'''Test for Operations'''
import pytest
from app.plugins.operations import Operations

@pytest.fixture
def operations():
    '''Fixture to provide an instance of Operations'''
    return Operations()  # Fixture provides an instance of Operations

def test_add(operations, first_number, second_number):
    '''checks addition operation'''
    result = operations.add(first_number, second_number)  # Call the method with 1st and 2nd number
    assert result == first_number + second_number

def test_subtract(operations, first_number, second_number):
    '''checks subtraction operation'''
    result = operations.subtract(first_number, second_number)  # Call the method with 1st and 2nd number
    assert result == first_number - second_number

def test_divide(operations, first_number, second_number):
    '''Checks division operation'''
    if second_number == 0:
        with pytest.raises(ValueError, match="Division by zero is not allowed"):
            operations.divide(first_number, second_number)
    else:
        result = operations.divide(first_number, second_number)
        assert result == first_number / second_number

def test_multiply(operations, first_number, second_number):
    '''checks multiplying operation'''
    result = operations.multiply(first_number, second_number)  # Call the method with 1st and 2nd number
    assert result == first_number * second_number
