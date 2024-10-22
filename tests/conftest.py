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
        
def create_test_data(num_records):
    '''creates test data'''
    for _ in range(num_records):
        a = fake.random_int(min=1, max=100)
        b = fake.random_int(min=1, max=100)
        yield a, b

