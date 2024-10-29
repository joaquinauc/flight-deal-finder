from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv("keys.env")

ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, flight_data):
        self.flight_data = flight_data

    def send_notification(self, lowest_price):
        if self.flight_data.price != "N/A" and self.flight_data.price < lowest_price:
            client = Client(ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(
                from_="whatsapp:+14155238886",
                body=f"Low price alert! Only ${self.flight_data.price} to fly from {self.flight_data.origin_airport} "
                     f"to {self.flight_data.destination_airport}, on {self.flight_data.out_date} to "
                     f"{self.flight_data.return_date}.",
                to="whatsapp:+5216442460105"
            )
