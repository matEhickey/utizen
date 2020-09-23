import os
from dotenv import load_dotenv
load_dotenv()

def get(key):
    return(os.getenv(key))