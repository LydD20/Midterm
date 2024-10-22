import pytest
from app.plugins.operations import Operations

def operations():
    '''runs Operations'''
    return Operations() #created function to limit repetition

def test_add(operations, a, b):
    '''checks addition operation'''
    result= operations.add
    assert result == a+b

def test_subtract(operations, a, b):
    '''checks subtraction operation'''
    result = operations.subtract(a,b)
    assert result == a-b

def test_divide(operations, a, b):
    '''checks division operation'''
    try:
        result = operations.divide(a,b)
        assert result == a/b
    except ValueError as e:
        assert str(e) == "Cannot divide by zero"

def test_multiply(operations, a, b):
    '''checks multiplying operation'''
    result = operations.multiply(a, b)
    assert result == a * b
    
    
