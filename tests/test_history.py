'''Test History'''
import pytest
from faker import Faker
from app.plugins.history import Manage_History

fake = Faker()

@pytest.fixture
def manage_history(tmp_path):
    '''Manages history using a temporary file'''
    filename = tmp_path / "history.csv"
    return Manage_History(filename)

def add_multiple_entries(manager, entries):
    '''Helper function to add multiple entries to history'''
    for data in entries:
        manager.save(data)

def assert_history_entry(loaded_history, entry_index, expected_data):
    '''Helper function to assert history entry matches expected data'''
    row = loaded_history.iloc[entry_index]
    assert row['name'] == expected_data['name']
    assert row['operation'] == expected_data['operation']
    assert int(row['result']) == expected_data['result']

def test_add_one_entry(manage_history):
    '''Test adding one entry to history'''
    entry_data = {
        'index': 1,
        'name': fake.name(),
        'operation': 'add',
        'result': fake.random_number(digits=3)
    }
    manage_history.save(entry_data)
    loaded_history = manage_history.load()

    assert len(loaded_history) == 1
    assert_history_entry(loaded_history, 0, entry_data)

def test_load_empty_history(manage_history):
    '''Tests loading from empty history'''
    loaded_history = manage_history.load()
    assert loaded_history.empty

def test_load_from_empty_existing_file(tmp_path):
    '''Tests loading history from an existing empty file'''
    empty_file = tmp_path / "empty.csv"
    empty_file.touch()  # Creates an empty file
    manager = Manage_History(empty_file)
    loaded_history = manager.load()

    assert loaded_history.empty

def test_remove_entry(manage_history):
    '''Tests removing entry from history'''
    entry1 = {
        'index': 1,
        'name': fake.name(),
        'operation': 'add',
        'result': fake.random_number(digits=3)
    }
    entry2 = {
        'index': 2,
        'name': fake.name(),
        'operation': 'subtract',
        'result': fake.random_number(digits=3)
    }
    add_multiple_entries(manage_history, [entry1, entry2])

    manage_history.delete(0)  # Removes the first entry
    loaded_history = manage_history.load()

    assert len(loaded_history) == 1  # Should contain only 1 entry after deletion
    assert_history_entry(loaded_history, 0, entry2)

def test_remove_nonexistent_entry(manage_history):
    '''Tests trying to remove nonexistent entry from history'''
    entry = {
        'index': 1,
        'name': fake.name(),
        'operation': 'add',
        'result': fake.random_number(digits=3)
    }
    manage_history.save(entry)

    manage_history.delete(5)
    loaded_history = manage_history.load()

    assert len(loaded_history) == 1

def test_clear_all_entries(manage_history):
    '''Tests clearing all entries from history'''
    entry = {
        'index': 1,
        'name': fake.name(),
        'operation': 'add',
        'result': fake.random_number(digits=3)
    }
    manage_history.save(entry)
    manage_history.clear()
    loaded_history = manage_history.load()

    assert loaded_history.empty  # Should be empty after clearing

# Additional tests for error handling

def test_load_history_file_not_exist(manage_history):
    '''Test loading history from a non-existent file'''
    manage_history.filename = "non_existent_file.csv"
    loaded_history = manage_history.load()

    # Assert that the history is empty when the file does not exist
    assert loaded_history.empty

def test_save_history_to_readonly_file(tmp_path):
    '''Test saving history to a read-only file'''
    readonly_file = tmp_path / "readonly.csv"
    readonly_file.touch(0o444)  # Set file as read-only
    manage_history = Manage_History(readonly_file)
    with pytest.raises(PermissionError):
        manage_history.save({
            'index': 1,
            'name': fake.name(),
            'operation': 'add',
            'result': fake.random_number(digits=3)
        })

def test_delete_nonexistent_entry(manage_history):
    '''Test deleting an entry that does not exist'''
    entry = {'index': 1, 'name': fake.name(), 'operation': 'add', 'result': fake.random_number(digits=3)}
    manage_history.save(entry)
    manage_history.delete(5)  # Trying to delete non-existent entry
    loaded_history = manage_history.load()
    assert len(loaded_history) == 1
