'''Manage History'''
import pandas as pd
import os
import logging

class Manage_History:
    def __init__(self, filename):
        self.filename = filename
        # defined columns for CSV
        self.columns = ['index', 'name', 'operation', 'result']

    def _file_existence(self):
        '''see if histoty file exists and isn't empty'''
        return os.path.exists(self.filename) and os.path.getsize(self.filename) >0
    
    def _initialize_file(self):
        '''initialize file with empty line if it doesn't exist'''
        if not self._file_existence():
            with open(self.filename, mode='w') as file:
                file.write('\n')
    
    def _loading_data(self):
        '''load CSV into a dataframe'''
        if self._file_existence():
            try:
                return pd.read_csv(self.filename)
            except pd.errors.EmptyDataError:
                return pd.DataFrame(columns= self.columns)
        return pd.DataFrame(columns=self.columns)

    def save(self, data):
        '''Saves results to CSV'''
        df= pd.DataFrame([data], columns=self.columns)
        self._initialize_file()
        df.to_csv(self.filename, mode='a', index=False, header=not self._file_exists())

    def load(self):
        '''Loads history from CSV'''
        return self._load_data()
    
    def delete(self, index):
        '''Delete a certain entry from history'''
        df = self._load_data()
        if df.empty:
            logging.error("Dataframe is empty, cannot delete.")
            return
        
        # Make sure index is within bounds
        if index <0 or index >= len(df):
            logging.error(f"Error. Index {index} is not in bounds. You must provide a valid index.")

        df = df.drop(index) #drops specific index
        df.reset_index(drop=True, inplace=True) #resets index after deletion
        df.to_csv(self.filename, index=False)
        logging.info(f"Record at index {index} deleted")

    def clear(self):
        '''clears history by deleted file'''
        if os.path.exists(self.filename):
            os.remove(self.filename)
            logging.info("History has been cleared.")
        else:
            logging.info("Not history file found, cannot clear.")