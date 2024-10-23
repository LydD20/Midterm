import logging
import os
import pandas as pd
from dotenv import load_dotenv
from app.plugins import Manage_Command

# Load environment variables
load_dotenv()

# Environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "production") 
LOG_PATH = os.getenv("LOG_PATH", "logs/app.log")
LOGGER_LEVEL = os.getenv("LOGGER_LEVEL", "INFO")
HISTORY_LOCATION = os.getenv("HISTORY_LOCATION", "data/balance.csv")

# Create logs directory if not exists
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# Configure logging
logging.basicConfig(
    level=LOGGER_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)

class App:
    def __init__(self):
        '''Initializes Program'''
        self.command_handler = Manage_Command()
        self.last_result = None
        self.history_file = HISTORY_LOCATION
        
        self._initialize_history_file()
        logging.info("Intialized App.")
    

    def _initialize_csv_with_headers(self):
        '''Creates an empty CSV file with headers.'''
        # Ensure the directory exists before creating the file
        directory = os.path.dirname(self.history_file)
        if not os.path.exists(directory):
            os.makedirs(directory)  # Create the directory if it doesn't exist

        # Define the headers for the CSV file
        headers = ['index', 'name', 'operation', 'result']
        
        # Create a DataFrame with the headers
        df = pd.DataFrame(columns=headers)
        
        # Write the DataFrame to the CSV file
        df.to_csv(self.history_file, index=False)
        
        # Log and print that the CSV has been initialized
        logging.info("CSV initialized with headers: %s", headers)
        print("Initialized CSV with headers.")

    def _initialize_history_file(self):
        '''Initializes history CSV file if it doesn't exist'''
        if not os.path.exists(self.history_file) or os.path.getsize(self.history_file) == 0:
            self._initialize_csv_with_headers()

    def start(self):
        '''Start the application loop.'''
        logging.info("Starting app.")
        name = self._get_user_name()
        logging.info(f"{name} entered the application")
        self._command_loop(name)

    def _get_user_name(self):
        '''Get the user's name from input.'''
        return input("Please input your name: ")

    def _command_loop(self, name):
        '''Command loop for user input'''
        commands = {
            "add": self._handle_operation,
            "subtract": self._handle_operation,
            "multiply": self._handle_operation,
            "divide": self._handle_operation,
            "save": self._save_history,
            "load": self._load_history,
            "delete": self._delete_history_entry,
            "clear": self._clear_history,
            "exit": self._log_and_exit
        }

        while True:
            command = self._get_input("Enter a command (add, subtract, divide, multiple, save, load, delete, clear, exit): ").lower()
            if command in commands:
                commands[command](command, name)
            else:
                print("Error. Invalid command. Try again.")

    def _log_and_exit(self, command, name=None):
        '''Log for exiting'''
        logging.info(f"{command} command received. Exiting application.")

    def _handle_operation(self, command, name=None):
        '''Perform operation based on command.'''
        logging.info(f"Performing operation: {command}")
        num1, num2 = self._get_two_numbers()
        result = self._execute_command(command, num1, num2)
        if result is not None:
            self.last_result = result
            print(f"Result: {result}")

    def _get_two_numbers(self):
        '''Get two numbers from the user for an operation.'''
        num1 = self._get_number("Insert first number: ")
        num2 = self._get_number("Insert second number: ")
        return num1, num2

    def _execute_command(self, command, num1, num2):
        '''Execute the command and handle errors.'''
        try:
            result = self.command_handler.execute_operation(command, num1, num2)
            logging.info(f"Operation result: {result}")
            return result
        except ValueError:
            logging.error("Invalid input. Insert valid numbers.")
            print("Error: Must insert valid numbers.")
            return None

    def _get_number(self, prompt):
        '''Get a number input from the user.'''
        try:
            return float(self._get_input(prompt))
        except ValueError:
            logging.error("Invalid input for number.")
            print("Error: Must insert valid number.")
            return self._get_number(prompt)

    def _save_history(self, command, name):
        '''Save the result to history.'''
        if self.last_result is not None:
            current_history = self.command_handler.load_history()
            new_index = len(current_history)
            self.command_handler.save_history({
                'index': new_index,  
                'name': name,
                'operation': "save",
                'result': self.last_result,
            })
            logging.info("History saved.")
            print("History saved.")
            self.last_result = None
        else:
            logging.warning("No result to save.")
            print("No results to save. You must perform an operation first.")

    def _load_history(self, command=None, name=None):
        '''Load and display history.'''
        history = self.command_handler.load_history()
        if history.empty:
            logging.info("Cannot locate history.")
            print("History is empty.")
        else:
            logging.info(f"Loaded history: \n{history}")
            print("Loaded history:\n", history.to_string(index=False))

    def _delete_history_entry(self, command=None, name=None):
        '''Delete an entry from history.'''
        index = self._get_valid_index()
        if index is not None:
            try:
                self.command_handler.delete_history(index)
                logging.info(f"Deleted history entry at index {index}.")
                print(f"Deleted entry at index {index}.")
            except Exception as e:
                logging.error(f"Error deleting history: {str(e)}")
                print(f"Error: {str(e)}")

    def _get_valid_index(self):
        '''Get a valid index from the user'''
        try:
            return int(self._get_input("Enter the index of the record to delete: "))
        except ValueError:
            logging.error("Invalid index input.")
            print("Error: You must enter a valid number for the index.")
            return None

    def _clear_history(self, command=None, name=None):
        '''Clear the entire history.'''
        self.command_handler.clear_history()
        logging.info("History cleared.")
        print("History cleared.")

    def _get_input(self, prompt):
        '''Grab input from the user.'''
        return input(prompt)