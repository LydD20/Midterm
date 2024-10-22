'''Configuration Test'''
import os
import logging
from faker import Faker
import pytest

fake = Faker()

@pytest.fixture(scope='session', autouse=True)
def setup_data_directory():
    '''checks data directory existence'''    
    if not os.path.exists('data'):
        os.makedirs('data')
        logging.info("Data directory created.")
    else:
        logging.info("Data directory already exists.")
<<<<<<< HEAD
        
=======
    

@pytest.fixture
def rand_numbers():
    '''creates random list of numbers 1 through 100'''
    num_records = 10
    data= []
    for _ in range(num_records):
        a= fake.random_int(min=1, max=100)
        b= fake.random_int(min=1, max=100)
        data.append((a, b))
    return data

@pytest.fixture
def records_num(pytestconfig):
    '''fixture to retrieve records_num value from command line'''
    return pytestconfig.getoption("records_num")

>>>>>>> testing
def create_test_data(num_records):
    '''creates test data'''
    for _ in range(num_records):
        a = fake.random_int(min=1, max=100)
        b = fake.random_int(min=1, max=100)
        yield a, b

<<<<<<< HEAD
=======
def pytest_addoption(parser):
    '''Adds pytest command line options'''
    parser.addoption("--records_num", action="store", default=5, type=int, help= "This is how many test records to create of test records.")

def pytest_create_tests(metafunc):
    '''Creates tests based on fixture'''
    if {"a", "b"}.issubset(metafunc.fixturenames):
        num_records = metafunc.config.getoption("records_num")
        test_data= create_test_data("records_num")
        metafunc.parametrize("a,b", test_data)
>>>>>>> testing
