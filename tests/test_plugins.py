'''Test Plugins'''
import pytest
from faker import Faker
from app.plugins import Manage_Command

fake = Faker()

@pytest.fixture
def manage_command_fix():
    '''Fixture for Managing Command'''
    return Manage_Command()  # Correctly instantiate the class

# Apply parametrize decorator to test plugins
@pytest.mark.parametrize("operation_name, expected_result", [
    ("add", lambda a, b: a + b),
    ("subtract", lambda a, b: a - b),
    ("multiply", lambda a, b: a * b)
])
def test_operations(manage_command_fix, rand_numbers, operation_name, expected_result):
    '''Test for adding, subtracting, and multiplying operations'''
    for a, b in rand_numbers:
        result = manage_command_fix.execute_operation(operation_name, a, b)
        assert result == expected_result(a, b)

def test_divide_operations(manage_command_fix, rand_numbers):
    '''Test division separately to deal with zero error'''
    for a, b in rand_numbers:
        if b != 0:
            result = manage_command_fix.execute_operation("divide", a, b)
            assert result == a / b
        else:
            with pytest.raises(ZeroDivisionError):
                manage_command_fix.execute_operation("divide", a, b)

def save_rand_history(manage_command_fix, rand_numbers):
    '''Helper function that saves random history for testing'''
    for indx, (a, b) in enumerate(rand_numbers):
        data = {
            'index': indx,
            'name': fake.name(),
            'operation': 'add',
            'result': a + b
        }
        manage_command_fix.save_history(data)  # Corrected to call save_history

def test_delete_history(manage_command_fix, rand_numbers):
    '''Tests deleting history'''
    save_rand_history(manage_command_fix, rand_numbers)
    prior_history = manage_command_fix.load_history()
    manage_command_fix.delete_history(0)  # this will delete first entry
    after_history = manage_command_fix.load_history()

    assert len(after_history) == len(prior_history) - 1  # takes away one entry

def test_clear_history(manage_command_fix, rand_numbers):
    '''Tests clearing history'''
    save_rand_history(manage_command_fix, rand_numbers)
    manage_command_fix.clear_history()
    history = manage_command_fix.load_history()
    assert history.empty
