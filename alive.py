# Import libs
import requests
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# ADSL TCI URL
tci_url = "https://adsl.tci.ir/panel/"

# Set cookie
headers = {
    "Cookie": os.getenv("TCI_COOKIE")
}

# Request
tci_raw = requests.get(tci_url, headers=headers)
