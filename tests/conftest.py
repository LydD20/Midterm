'''Configuration Test'''
import os
import logging
import pytest
from faker import Faker
from app.plugins.operations import Operations

fake = Faker()

# Fixture to ensure data directory is created and cleaned up
@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_data_directory():
    '''Ensure data directory is created and cleaned up'''
    if not os.path.exists('data'):
        os.makedirs('data')
        logging.info("Data directory created.")
    else:
        logging.info("Data directory already exists.")
    yield  # Tests using this fixture will run here

    # Cleanup: remove the directory after tests
    if os.path.exists('data'):
        os.rmdir('data')
        logging.info("Data directory removed after tests.")

# Fixture for random numbers
@pytest.fixture
def rand_numbers():
    '''creates random list of numbers 1 through 100'''
    num_records = 10
    data = []
    for _ in range(num_records):
        first_number = fake.random_int(min=1, max=100)
        second_number = fake.random_int(min=1, max=100)
        data.append((first_number, second_number))
    return data

# Fixture to provide an instance of the Operations class
@pytest.fixture
def operations():
    '''Fixture to provide an instance of the Operations class'''
    return Operations()

# Fixture to retrieve records_num value from command line
@pytest.fixture
def records_num(pytestconfig):
    '''fixture to retrieve records_num value from command line'''
    return pytestconfig.getoption("records_num")

# Function to generate test data
def generate_test_data(num_records):
    '''creates test data'''
    for _ in range(num_records):
        first_number = fake.random_int(min=1, max=100)
        second_number = fake.random_int(min=1, max=100)
        yield first_number, second_number

# Adds pytest command line options
def pytest_addoption(parser):
    '''Adds pytest command line options'''
    parser.addoption("--records_num", action="store", default=5, type=int, help="How many test records to create.")

# Generates tests based on fixture
def pytest_generate_tests(metafunc):
    '''Creates tests based on fixture'''
    if {"first_number", "second_number"}.issubset(metafunc.fixturenames):
        num_records = metafunc.config.getoption("records_num")
        test_data = generate_test_data(num_records)
        metafunc.parametrize("first_number,second_number", test_data)

# Additional Tests Integrated into conftest.py

# Test the rand_numbers fixture
def test_rand_numbers(rand_numbers):
    '''Test the rand_numbers fixture'''
    assert len(rand_numbers) == 10  # Make sure the fixture returns 10 records
    for first_number, second_number in rand_numbers:
        assert isinstance(first_number, int)
        assert isinstance(second_number, int)
        assert 1 <= first_number <= 100
        assert 1 <= second_number <= 100

# Test that the records_num option works
def test_records_num(records_num):
    '''Test that the records_num option works'''
    assert isinstance(records_num, int)
    assert records_num >= 0

# Test the generated test data
def test_generated_tests(first_number, second_number):
    '''Test the generated test data'''
    assert isinstance(first_number, int)
    assert isinstance(second_number, int)
    assert 1 <= first_number <= 100
    assert 1 <= second_number <= 100

# Test logging for setup and teardown of data directory
def test_logging_setup_and_teardown_data_directory(caplog):
    '''Test logging for setup and teardown of data directory'''
    with caplog.at_level(logging.INFO):
        assert 'Data directory already exists.' in caplog.text or 'Data directory created.' in caplog.text
