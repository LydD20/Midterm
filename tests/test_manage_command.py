'''Tests the Class Manage_Command'''
from unittest.mock import MagicMock
import pytest
from app import Manage_Command

@pytest.fixture
def manage_command():
    '''Fixture for Manage_Command'''
    return Manage_Command("test_history.csv")

### 1. Tests for Invalid Arguments and Operations

def test_invalid_operation_name(manage_command):
    '''Test for invalid operation name'''
    with pytest.raises(ValueError, match="Unknown mathematical operation"):
        manage_command.execute_operation("invalid_op", 5, 3)

def test_operation_missing_arguments(manage_command):
    '''Test for missing arguments in operations'''
    with pytest.raises(ValueError, match="requires exactly two arguments"):
        manage_command.execute_operation("add", 5)  # Missing second argument

def test_operation_extra_arguments(manage_command):
    '''Test for too many arguments in operations'''
    with pytest.raises(ValueError, match="requires exactly two arguments"):
        manage_command.execute_operation("add", 5, 3, 2)  # Extra argument

def test_empty_operation_name(manage_command):
    '''Test that empty operation name raises ValueError'''
    with pytest.raises(ValueError, match="Unknown mathematical operation"):
        manage_command.execute_operation("", 1, 2)

def test_operation_with_single_argument(manage_command):
    '''Test that passing only one argument raises ValueError'''
    with pytest.raises(ValueError, match="requires exactly two arguments"):
        manage_command.execute_operation("add", 5)

def test_operation_with_extra_arguments(manage_command):
    '''Test that passing more than two arguments raises ValueError'''
    with pytest.raises(ValueError, match="requires exactly two arguments"):
        manage_command.execute_operation("add", 1, 2, 3)

def test_operation_with_non_numeric_values(manage_command):
    '''Test that passing non-numeric values raises TypeError'''
    with pytest.raises(TypeError):
        manage_command.execute_operation("multiply", "a", 2)

def test_unknown_operation(manage_command):
    '''Test that an unknown operation raises ValueError'''
    with pytest.raises(ValueError, match="Unknown mathematical operation"):
        manage_command.execute_operation("unknown", 1, 2)

def test_divide_by_zero(manage_command):
    '''Test division by zero raises an error'''
    with pytest.raises(ValueError, match="Division by zero is not allowed"):
        manage_command.execute_operation("divide", 10, 0)

### 2. Tests for History Functionality

def test_save_history_calls(manage_command):
    '''Test save history is called with correct data'''
    manage_command.manage_history.save = MagicMock()
    history_data = {"index": 1, "name": "test", "operation": "add", "result": 5}
    manage_command.save_history(history_data)
    manage_command.manage_history.save.assert_called_with(history_data)

def test_load_history_calls(manage_command):
    '''Test load history is called correctly'''
    manage_command.manage_history.load = MagicMock(return_value=[{"index": 1}])
    history = manage_command.load_history()
    manage_command.manage_history.load.assert_called_once()
    assert len(history) == 1

def test_delete_history_calls(manage_command):
    '''Test delete history with valid index'''
    manage_command.manage_history.delete = MagicMock()
    manage_command.delete_history(0)
    manage_command.manage_history.delete.assert_called_with(0)

def test_clear_history_calls(manage_command):
    '''Test clear history is called correctly'''
    manage_command.manage_history.clear = MagicMock()
    manage_command.clear_history()
    manage_command.manage_history.clear.assert_called_once()

def test_save_empty_history(manage_command):
    '''Test saving an empty history'''
    manage_command.manage_history.save = MagicMock()
    empty_data = {}
    manage_command.save_history(empty_data)
    manage_command.manage_history.save.assert_called_with(empty_data)

def test_load_empty_history_file(manage_command):
    '''Test loading from an empty history file'''
    manage_command.manage_history.load = MagicMock(return_value=[])
    history = manage_command.load_history()
    assert history == []

### 3. Tests for Edge Cases

def test_delete_history_invalid_index(manage_command):
    '''Test delete history with invalid index'''
    manage_command.manage_history.delete = MagicMock()
    manage_command.delete_history(999)  # Index out of bounds
    manage_command.manage_history.delete.assert_called_with(999)

def test_delete_negative_index(manage_command):
    '''Test delete history with negative index'''
    manage_command.manage_history.delete = MagicMock()
    manage_command.delete_history(-1)  # Negative index
    manage_command.manage_history.delete.assert_called_with(-1)

def test_load_empty_history(manage_command):
    '''Test loading empty history'''
    manage_command.manage_history.load = MagicMock(return_value=[])
    result = manage_command.load_history()
    assert result == []

def test_delete_history_empty_file(manage_command):
    '''Test deleting history from an empty history file'''
    manage_command.manage_history.delete = MagicMock()
    manage_command.delete_history(0)  # Attempt to delete from an empty history
    manage_command.manage_history.delete.assert_called_with(0)

### 4. Test for Large Data Operations

def test_large_history_data(manage_command):
    '''Test handling large history data'''
    large_data = [{"index": i, "name": f"Entry {i}", "operation": "add", "result": i} for i in range(1000)]
    manage_command.manage_history.load = MagicMock(return_value=large_data)
    result = manage_command.load_history()
    assert len(result) == 1000

def test_large_data_save_history(manage_command):
    '''Test saving a large history entry'''
    large_entry = {'index': 1000, 'name': 'Large Test', 'operation': 'add', 'result': 99999}
    manage_command.manage_history.save = MagicMock()
    manage_command.save_history(large_entry)
    manage_command.manage_history.save.assert_called_with(large_entry)

### 5. Test for Operations with Large Numbers

@pytest.mark.parametrize("operation_name, first_value, second_value, expected", [
    ("add", 1000000, 2000000, 3000000),
    ("subtract", 2000000, 1000000, 1000000),
    ("multiply", 1000000, 2, 2000000),
    ("divide", 1000000, 2, 500000),
])
def test_large_number_operations(manage_command, operation_name, first_value, second_value, expected):
    '''Test operations with large numbers'''
    result = manage_command.execute_operation(operation_name, first_value, second_value)
    assert result == expected

### 6. Test File Handling and Data Integrity

def test_load_history_file_not_found(manage_command):
    '''Test loading history when file is not found'''
    manage_command.manage_history.load = MagicMock(side_effect=FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        manage_command.load_history()

def test_save_history_permission_denied(manage_command):
    '''Test saving history when permission is denied'''
    manage_command.manage_history.save = MagicMock(side_effect=PermissionError)
    with pytest.raises(PermissionError):
        manage_command.save_history({'index': 1, 'name': 'Test', 'operation': 'add', 'result': 5})

def test_history_data_integrity(manage_command):
    '''Test data integrity by saving and loading multiple times'''
    data = {"index": 1, "name": "Test", "operation": "add", "result": 5}
    manage_command.save_history(data)
    manage_command.save_history({"index": 2, "name": "Test2", "operation": "subtract", "result": 3})
    manage_command.manage_history.load = MagicMock(return_value=[data, {"index": 2, "name": "Test2", "operation": "subtract", "result": 3}])
    history = manage_command.load_history()
    assert len(history) == 2
    assert history[0]["result"] == 5
    assert history[1]["result"] == 3
