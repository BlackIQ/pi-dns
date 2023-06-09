# Import libs
from bs4 import BeautifulSoup
import requests
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Get the values of the required environment variables
api_token = os.getenv("CLOUDFLARE_TOKEN")
zone_id = os.getenv("CLOUDFLARE_ZONE")

# Set the domain name and record type
dns_name = os.getenv("CLOUDFLARE_DNS")
record_type = 'A'


def get_public_ip():
    # ADSL TCI URL
    tci_url = "https://adsl.tci.ir/panel/"

    # Set cookie
    headers = {
        "Cookie": os.getenv("TCI_COOKIE")
    }

    # Request
    tci_raw = requests.get(tci_url, headers=headers)

    # Parse in HTML
    soup = BeautifulSoup(tci_raw.content, 'html.parser')

    # Find IP
    ip = soup.select_one(
        'table.uk-table.uk-table-striped tr td:last-child b').text

    # Return IP
    return ip


# Get public IP
public_ip = get_public_ip()

# Define the URL for the Cloudflare API endpoint
url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type={record_type}&name={dns_name}"

# Set the API request headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_token}'
}

# Make the API request and get the response JSON
response = requests.get(url, headers=headers)
response_json = response.json()

# Extract the current IP address from the DNS record
current_ip_address = response_json['result'][0]['content']

# Check if the IP address has changed
if public_ip != current_ip_address:
    # If the IP address has changed, update the DNS record
    dns_record_id = response_json['result'][0]['id']
    update_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_record_id}"
    data = {
        "type": "A",
        "name": dns_name,
        "content": public_ip,
        "ttl": 1,
        "proxied": False
    }

    requests.put(update_url, headers=headers, json=data)

    print(f"DNS record updated: {dns_name} now points to {public_ip}")
else:
    # If the IP address hasn't changed, do nothing
    print("IP address has not changed.")
