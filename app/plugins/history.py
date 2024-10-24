'''Manage History'''
import os
import pandas as pd
import logging

class Manage_History:
    def __init__(self, filename):
        self.filename = filename
        self.columns = ['index', 'name', 'operation', 'result']

    def _file_exists(self):
        '''Check if history file exists'''
        return os.path.exists(self.filename)
    
    def _load_data(self):
        '''Load CSV into a DataFrame'''
        if not self._file_exists():
            # Instead of raising FileNotFoundError, return an empty DataFrame
            logging.info(f"File {self.filename} does not exist, returning an empty DataFrame.")
            return pd.DataFrame(columns=self.columns)

        try:
            return pd.read_csv(self.filename)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=self.columns)

    def save(self, data):
        '''Saves results to CSV'''
        df = pd.DataFrame([data], columns=self.columns)
        
        # Check if file exists and write the header if new
        header_needed = not self._file_exists()
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
        
        if index < 0 or index >= len(df):
            logging.error(f"Error. Index {index} is out of bounds.")
            return

        df = df.drop(index)
        df.reset_index(drop=True, inplace=True)
        df.to_csv(self.filename, index=False)
        logging.info(f"Record at index {index} deleted")

    def clear(self):
        '''Clear history by deleting the file'''
        if self._file_exists():
            os.remove(self.filename)
            logging.info(f"History cleared: {self.filename}")
        else:
            logging.info(f"File {self.filename} does not exist.")
