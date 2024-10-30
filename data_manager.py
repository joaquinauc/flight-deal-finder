import requests
import os
from dotenv import load_dotenv

load_dotenv("keys.env")

PRICES_ENDPOINT = os.environ.get("PRICES_ENDPOINT")
USERS_ENDPOINT = os.environ.get("USERS_ENDPOINT")


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheet_data = {}

    def read_data(self):
        read_sheet = requests.get(PRICES_ENDPOINT).json()
        self.sheet_data = read_sheet["prices"]
        # print(self.sheet_data)
        return self.sheet_data

    def write_data(self):
        for data in self.sheet_data:
            new_data = {
                "price": {
                    "iataCode": data["iataCode"]
                }
            }
            response = requests.put(f"{PRICES_ENDPOINT}/{data["id"]}", json=new_data)
            print(response.text)


def get_customer_emails():
    users_data = requests.get(USERS_ENDPOINT).json()
    read_emails = users_data["users"]
    return read_emails
