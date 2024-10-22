import logging
import os
from dotenv import load_dotenv


load_dotenv() #load .env file in

def setup_logger (name="calculator"):
    '''sets logger up based on environment variables'''

    #retrieves log level and log path from .env
    LOGGER_LEVEL= os.getenv("LOGGER_LEVEL", "INFO").upper()
    LOG_PATH= os.getenv("LOG_PATH", "logs/app.log")

    # Creates logger
    logger = logging.getLogger(name)
    logger.setLevel(LOGGER_LEVEL)

    #Checks if handlers have been added to avoid duplicates
    if not logger.hasHandlers():
        #creates file handler for log messages to file specified
        file_handler= logging.FileHandler(LOG_PATH)
        file_handler.setLevel(LOGGER_LEVEL)

        #creates console handler to ouput logs
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOGGER_LEVEL)

        #define logging format
        formatter= logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        #Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()

