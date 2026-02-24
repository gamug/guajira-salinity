import os, sys

sys.path.append(os.path.join(os.getcwd(), 'src'))
from dotenv import load_dotenv

from src.data_processing import process_data
load_dotenv()

if __name__=='__main__':
    process_data()