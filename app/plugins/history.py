'''Manage History'''
import os
import pandas as pd
import logging

class Manage_History:
    def __init__(self, filename):
        self.filename = filename
        self.columns = ['index', 'name', 'operation', 'result']

    def _file_exists(self):
        '''Check if history file exists and isn't empty'''
        return os.path.exists(self.filename) and os.path.getsize(self.filename) > 0
    
    def _initialize_file(self):
        '''Initialize file with an empty line if it doesn't exist'''
        if not self._file_exists():
            with open(self.filename, mode='w') as file:
                file.write('\n')
    
    def _load_data(self):
        '''Load CSV into a DataFrame'''
        if self._file_exists():
            try:
                return pd.read_csv(self.filename)
            except pd.errors.EmptyDataError:
                return pd.DataFrame(columns=self.columns)
        return pd.DataFrame(columns=self.columns)

    def save(self, data):
        '''Saves results to CSV'''
        # Convert the data to a DataFrame
        df = pd.DataFrame([data], columns=self.columns)
    
        self._initialize_file()
        
        # Check if file exists, and write the header only if the file is new 
        header_needed = not self._file_exists()
        
        # Append to the file, and write header only if it's the first write
        df.to_csv(self.filename, mode='a', index=False, header=header_needed)
        
        logging.info(f"Data saved to {self.filename}: {data}")


    def load(self):
        '''Load history from CSV'''
        df = self._load_data()
        logging.info(f"Data loaded from {self.filename}: {df}")
        return df
    
    def delete(self, index):
        '''Delete a specific entry from history'''
        df = self._load_data()
        if df.empty:
            logging.error("Dataframe is empty, cannot delete.")
            return
        
        # Make sure index is within bounds
        if index < 0 or index >= len(df):
            logging.error(f"Error. Index {index} is out of bounds. Must provide a valid index.")
            return

        df = df.drop(index)  # Drops specific index
        df.reset_index(drop=True, inplace=True)  # Resets index after deletion
        df.to_csv(self.filename, index=False)
        logging.info(f"Record at index {index} deleted")

    def clear(self):
        '''Clear history by deleting the file'''
        if os.path.exists(self.filename):
            os.remove(self.filename)
            logging.info(f"History cleared: {self.filename}")
        else:
            logging.info(f"No history file found, cannot clear.")
