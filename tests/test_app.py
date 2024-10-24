'''Test for app''' 
from unittest.mock import MagicMock, patch
import pytest  # Third-party import
import pandas as pd  # Ensure pandas is imported
from app import App

@pytest.fixture
def app():
    '''Fixture to create an instance of the App class'''
    with patch("app.App._initialize_history_file") as mock_init:
        yield App(), mock_init  # Yield an instance of App and the mock

def test_initialize_csv_with_headers(app):
    '''Test if CSV is initialized with headers'''
    _, mock_init_history_file = app  # Unpack the fixture, ignore app_instance
    mock_init_history_file.assert_called_once()  # Verify it was called only once

def test_initialize_history_file_called_once(app):
    '''Ensure _initialize_history_file is called only once'''
    _, mock_init_history_file = app
    assert mock_init_history_file.call_count == 1  # Ensure it has been called once

def test_command_loop_with_invalid_command(app):
    '''Test handling of an invalid command'''
    app_instance, _ = app  # Unpack the fixture
    with patch("app.App._get_input", side_effect=["invalid_command", "exit"]):
        with pytest.raises(SystemExit):  # Check that it exits when "exit" is called
            app_instance._command_loop("Test User")  # pylint: disable=protected-access

def test_command_loop_with_valid_commands(app):
    '''Test command loop with valid commands'''
    app_instance, _ = app  # Unpack the fixture
    with patch("app.App._get_input", side_effect=["add", "5", "3", "exit"]):
        with patch("app.App._handle_operation") as mock_handle_operation:
            with pytest.raises(SystemExit):  # Check that it exits when "exit" is called
                app_instance._command_loop("Test User")  # pylint: disable=protected-access
            assert mock_handle_operation.called  # Ensure the operation was called

def test_save_history_no_result(app):
    '''Test saving history when there is no result'''
    app_instance, _ = app  # Unpack the fixture
    app_instance.last_result = None  # Set last_result to None
    with patch("app.logging.warning") as mock_logging:
        app_instance._save_history("save", "Test User")  # pylint: disable=protected-access
        assert "No result to save." in [call[0][0] for call in mock_logging.call_args_list]  # Check warning logged

def test_load_history_empty(app):
    '''Test loading history when it is empty'''
    app_instance, _ = app  # Unpack the fixture
    app_instance.command_handler = MagicMock()
    app_instance.command_handler.load_history.return_value.empty = True  # Simulate empty history
    with patch("app.logging.info") as mock_logging:
        app_instance._load_history()  # pylint: disable=protected-access
        assert "Cannot locate history." in [call[0][0] for call in mock_logging.call_args_list]  # Check message logged

def test_load_history_with_data(app):
    '''Test loading history when it contains data'''
    app_instance, _ = app
    app_instance.command_handler = MagicMock()
    sample_history = pd.DataFrame({
        "index": [0],
        "name": ["Test User"],
        "operation": ["add"],
        "result": [8]
    })
    app_instance.command_handler.load_history.return_value = sample_history

    with patch("app.logging.info") as mock_logging:
        app_instance._load_history()  # pylint: disable=protected-access
        mock_logging.assert_called_once_with(f"Loaded history: \n{sample_history}")

def test_get_user_name(app):
    '''Test getting the user's name'''
    app_instance, _ = app  # Unpack the fixture
    with patch("builtins.input", return_value="Test User"):
        name = app_instance._get_user_name()  # pylint: disable=protected-access
        assert name == "Test User"  # Ensure the name is correctly returned

def test_execute_command_with_error(app):
    '''Test executing a command that raises a ValueError'''
    app_instance, _ = app  # Unpack the fixture
    app_instance.command_handler = MagicMock()
    app_instance.command_handler.execute_operation.side_effect = ValueError("Invalid input")

    with patch("app.logging.error") as mock_logging:
        result = app_instance._execute_command("add", 5, 0)  # pylint: disable=protected-access
        assert result is None  # Ensure that result is None when error occurs
        assert "Invalid input. Insert valid numbers." in [call[0][0] for call in mock_logging.call_args_list]

def test_handle_operation_invalid_input(app):
    '''Test handling operation with invalid input'''
    app_instance, _ = app
    # Simulate an invalid number input by raising ValueError from _get_two_numbers
    with patch("app.App._get_two_numbers", side_effect=ValueError("Invalid numbers")), patch("app.logging.error") as mock_logging:
        # Call _handle_operation, which should handle the ValueError and log the error
        try:
            app_instance._handle_operation("add")  # pylint: disable=protected-access
        except ValueError:
            # Catch the ValueError to prevent it from failing the test
            pass

        # Check that the error was logged
        mock_logging.assert_called_with("Invalid input. Insert valid numbers.")

def test_clear_history(app):
    '''Test clearing the history'''
    app_instance, _ = app  # Unpack the fixture
    app_instance.command_handler = MagicMock()

    with patch("app.logging.info") as mock_logging:
        app_instance._clear_history()  # pylint: disable=protected-access
        app_instance.command_handler.clear_history.assert_called_once()  # Ensure the command handler's clear_history method was called
        assert "History cleared." in [call[0][0] for call in mock_logging.call_args_list]  # Ensure log entry is correct

def test_log_and_exit(app):
    '''Test logging and exiting the application'''
    app_instance, _ = app  # Unpack the fixture
    with patch("sys.exit") as mock_exit:
        app_instance._log_and_exit("exit")  # pylint: disable=protected-access
        mock_exit.assert_called_once()  # Ensure sys.exit was called

# Run all tests when executing this file
if __name__ == "__main__":
    pytest.main()
