# Calculator App
## Midterm Project
### by Lydia Daids

## Project Description
For this project, I created a console-based calculator application that performs simple operations (addition, subtraction, division, multiplication) and history management (save, load, delete, clear operations). This application was created using Python and implementing design patterns such as facade, command, and factor. To help with debugging, dynamic logging was incorporated into the code.

## Setup Instructions
### Requirements:
* Python 3.10+
* virtual environment

## Installation:
1. clone the repository:
```
git clone https://github.com/LydD20/midterm.git
cd calc_app
```
2. Set up virtual environment
```
python -m venv .venv
source .venv/bin/activate
```
3. Install necessary dependencies:
```
pip install -r requirements.txt
```
4. Create a .env file in root directory and configure the following 
```
environment variables:
ENVIRONMENT=development
LOGGER_LEVEL=INFO
LOG_PATH=logs/app.log
HISTORY_LOCATION=data/balance.csv
```
5. Run tests by typing:
```
pytest
```
6. Initialize the application:
```
python main.py
```

## Usage Examples:
# Simple Operations
After the application starts, it will prompt users to input their name. Then users will choose a simple operation. The operation options are as follows:

1. **Add Command:**
  * Example:
  ```
  Enter a command (add, subtract, divide, multiply, save, load, delete, clear, exit): **add**
  Insert first number: 3
  Insert second number: 4
  Result: 7
  ```
2. **Subtract Command**
  * Example:
  ```
  Enter a command (add, subtract, divide, multiply, save, load, delete, clear, exit): **subtract**
  Insert first number: 4
  Insert second number: 3
  Result: 1
  ```
3. **Divide Command**
  * Example:
  ```
  Enter a command (add, subtract, divide, multiply, save, load, delete, clear, exit): **divide**
  Insert first number: 3
  Insert second number: 4
  Result: 0.75
  ```
4. **Multiply Command**
  * Example:
  ```
  Enter a command (add, subtract, divide, multiply, save, load, delete, clear, exit): **multiply**
  Insert first number: 3
  Insert second number: 4
  Result: 12
  ```
## Managing History
In the application, users can also manage their history of calculations with the following commands:

1. Save: this will save the last result to the history file
```
Enter a command (add, subtract, divide, multiply, save, load, delete, clear, exit):  save
History saved.
```
2. Load: this will load all of the past saved operations from the history file
```
Enter a command (add, subtract, divide, multiply, save, load, delete, clear, exit):  load
Loaded history:
 index   name    operation   result
   0     Lydia     add         7
   1     Sam      subtract     1
```
3. Delete: this will delete the entry from the history file specified by its index.
```
Enter a command (add, subtract, divide, multiply, save, load, delete, clear, exit):  delete
Enter the index of the record to delete: 1
Loaded history:
 index   name    operation   result
   0     Lydia     add         7
```
4. Clear: this will clear all of the entries in the history file.
```
Enter a command (add, subtract, divide, multiply, save, load, delete, clear, exit): clear
History cleared.
```
5. Exit: this exits the application
```
Enter a command (add, subtract, divide, multiply, save, load, delete, clear, exit): exit
```
## Architectural Decisions
## Design Patterns
### Command Pattern
The **Command Pattern** is used throught the design of this application. Each operation was treated as a command and incorporated through the Manage_Command class, which is the initiator, and the Operations class, which acts to provide the implementations for the commands. The application is also extremely flexible if more operations were added, specifically because of the operation_map in Manage_Command. 
### Facade Pattern
The **Facade Pattern** is used in managing the history, specifically the class Manage_History. It provides a simplified interface for the history operations. It also manages file operations, to make sure the CSV file is correctly loaded and updated. This helps to hide the complexity of file handling while ensuring the rest of the application functions correctly.
### Singleton Pattern
The **Singleton Pattern** is used in the logging configuration with the setup_logger function which ensures only one logger is created during the application's cycle. This same logger is the reused across different modules. This design patterns helps get rid of multiple instances of the logger and ensure all parts of the application are consistent.

## Logging Strategy
The logging strategy for this application was to ensure logs were at every crucial part of the application. The application logs messages at different levels (INFO, ERROR, WARNING) to the log file and console. Some of the major points logging was used was during the initialization of the app and also whenever a command was typed in order to track the flow of the application. I also added logs in to track invalid inputs or exceptions and to help improve testing coverage. 





