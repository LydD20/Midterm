from app.plugins.history import Manage_History
from app.plugins.operations import Operations

class Manage_Command:
    def __init__(self, history_file="data/balance.csv"):
        '''Initializes the class Manage_Command with Plugins'''
        self.manage_history = Manage_History(history_file)

        # Initialize operations as an instance of the Operations class
        self.operations = Operations()

        self.operation_map = {
            "add": self.operations.add,
            "subtract": self.operations.subtract,
            "divide": self.operations.divide,
            "multiply": self.operations.multiply
        }

    def execute_operation(self, operation_name, *args):
        '''Executes math operation and returns result'''
        operation = self.operation_map.get(operation_name)

        # Checks to ensure two arguments are passed
        if len(args) != 2:
            raise ValueError(f"{operation_name} operation requires exactly two arguments, but {len(args)} were provided.")

        if operation:
            return operation(*args)  # Call the operation with the provided arguments
        raise ValueError(f"Unknown mathematical operation: {operation_name}")
    
    def save_history(self, data):
        '''Saves results to CSV'''
        self.manage_history.save(data)

    def load_history(self):
        '''Loads in history from CSV'''
        return self.manage_history.load()
    
    def delete_history(self, index):
        '''Deletes specified entry'''
        self.manage_history.delete(index)

    def clear_history(self):
        '''Clears history'''
        self.manage_history.clear()

        # Static method: checks if the operation name is valid
    @staticmethod
    def is_valid_operation(operation_name):
        '''Check if the given operation name is valid'''
        return operation_name in ["add", "subtract", "divide", "multiply"]

    # Class method: return all available operations
    @classmethod
    def available_operations(cls):
        '''Returns a list of available operations'''
        return ["add", "subtract", "divide", "multiply"]