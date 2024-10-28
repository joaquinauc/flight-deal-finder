import requests
import os
from dotenv import load_dotenv

load_dotenv("keys.env")

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
AMADEUS_ENDPOINT = "https://test.api.amadeus.com/"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.auth_headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.auth_parameters = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        self.cities_headers = {}

    def get_token(self):
        auth_response = requests.post(url=f"{AMADEUS_ENDPOINT}v1/security/oauth2/token", headers=self.auth_headers, data=self.auth_parameters).json()
        self.cities_headers["Authorization"] = auth_response["token_type"] + " " + auth_response["access_token"]

    def get_iata(self, city):
        self.get_token()
        cities_params = {
            "keyword": city
        }
        cities_response = requests.get(url=f"{AMADEUS_ENDPOINT}v1/reference-data/locations/cities", headers=self.cities_headers, params=cities_params).json()
        print(cities_response["data"][0]["iataCode"])
        return cities_response["data"][0]["iataCode"]

    def get_offers(self, iata_code, from_date, to_date, max_price):
        self.get_token()
        offers_params = {
            "originLocationCode": "LHR",
            "destinationLocationCode": iata_code,
            "departureDate": from_date,
            "returnDate": to_date,
            "adults": 1,
            "currencyCode": "USD",
        }
        response = requests.get(f"{AMADEUS_ENDPOINT}v2/shopping/flight-offers", headers=self.cities_headers, params=offers_params).json()
        return response


