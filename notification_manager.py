from twilio.rest import Client
import smtplib
import os
from dotenv import load_dotenv

load_dotenv("keys.env")

ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self, flight_data, emails):
        self.flight_data = flight_data
        self.emails = emails

    def send_notification(self, lowest_price):
        if self.flight_data.price != "N/A" and self.flight_data.price < lowest_price:
            client = Client(ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            client.messages.create(
                from_="whatsapp:+14155238886",
                body=f"Low price alert! Only ${self.flight_data.price} to fly from {self.flight_data.origin_airport}"
                     f"to {self.flight_data.destination_airport}, on {self.flight_data.out_date} to "
                     f"{self.flight_data.return_date}.",
                to="whatsapp:+5216442460105"
            )

    def send_emails(self, lowest_price):
        subject = "GET ON VACATION NOW!"
        body = f"Low price alert! Only ${self.flight_data.price} to fly from {self.flight_data.origin_airport}"\
               f"to {self.flight_data.destination_airport}, on {self.flight_data.out_date} to "\
               f"{self.flight_data.return_date}."
        msg = f"Subject: {subject}\n\n{body}"  # The \n\n is to write the body of the msg, it recognizes it as such.

        if self.flight_data.price != "N/A" and self.flight_data.price < lowest_price:
            with smtplib.SMTP("smtp-mail.outlook.com", port=587) as connection:
                connection.starttls()  # It makes the connection secure
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL, to_addrs=self.emails, msg=msg)
                connection.close()
