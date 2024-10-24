import pytest
from unittest.mock import patch, MagicMock
from app import App

@pytest.fixture
def test_initialize_app():
    app = App()
    app.start()


def test_initialize_csv_with_headers(app):
    '''Test if CSV is initialized with headers'''
    with patch("app.App._initialize_csv_with_headers") as mock_init_csv:
        app._initialize_history_file()
        mock_init_csv.assert_called_once()

def test_start_method(app):
    '''Test the start method to ensure it initializes and starts the command loop'''
    with patch("app.App._get_user_name", return_value="Test User"):
        with patch("app.App._command_loop") as mock_command_loop:
            app.start()
            mock_command_loop.assert_called_once()

def test_get_user_name(app):
    '''Test getting the user's name'''
    with patch("builtins.input", return_value="Test User"):
        name = app._get_user_name()
        assert name == "Test User"

def test_handle_operation_add(app):
    '''Test handling an addition operation'''
    with patch("app.App._get_two_numbers", return_value=(5, 3)):
        with patch("app.App._execute_command", return_value=8):
            with patch("app.logging.info"):
                app._handle_operation("add")
                assert app.last_result == 8

def test_save_history(app):
    '''Test saving history'''
    app.last_result = 10
    app.command_handler = MagicMock()
    app.command_handler.load_history.return_value = []
    
    with patch("app.logging.info"):
        app._save_history("save", "Test User")
        app.command_handler.save_history.assert_called_once_with({
            'index': 0,
            'name': "Test User",
            'operation': "save",
            'result': 10
        })

def test_load_history(app):
    '''Test loading history'''
    app.command_handler = MagicMock()
    app.command_handler.load_history.return_value = pd.DataFrame([{"index": 0, "name": "Test User", "operation": "add", "result": 10}])
    
    with patch("app.logging.info"):
        app._load_history()
        app.command_handler.load_history.assert_called_once()
