# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the
# program requirements.
from data_manager import DataManager, get_customer_emails
from flight_search import FlightSearch
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
import time

data_manager = DataManager()
flight_search = FlightSearch()

sheet_data = data_manager.read_data()

# Filling the IATA Code column with its respective codes
# for data in sheet_data:
#     # Modifying sheet_data with IATA Codes
#     data["iataCode"] = flight_search.get_iata(data["city"])
# data_manager.sheet_data = sheet_data
# data_manager.write_data()

today = datetime.now()

date_tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
date_after_six_months = (today + timedelta(days=182)).strftime("%Y-%m-%d")

customer_data = get_customer_emails()
customer_emails = [email["whatIsYourEmail?"] for email in customer_data]

for data in sheet_data:
    flights = flight_search.get_offers(data["iataCode"], date_tomorrow, date_after_six_months)

    try:
        if "data" not in flights:
            raise KeyError("No data found in the response.")
        cheapest_flight = find_cheapest_flight(flights)
    except KeyError:
        flights = flight_search.get_offers(data["iataCode"], date_tomorrow, date_after_six_months, False)
        if "data" in flights:
            cheapest_flight = find_cheapest_flight(flights)
    else:
        print(f"No flight data found for {data["iataCode"]}, searching for the next destination...")
        continue

    print(f"Lowest price from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}: ${cheapest_flight.price}")
    notif_manager = NotificationManager(cheapest_flight, customer_emails)
    notif_manager.send_notification(data["lowestPrice"])
    notif_manager.send_emails(data["lowestPrice"])
    time.sleep(2)
