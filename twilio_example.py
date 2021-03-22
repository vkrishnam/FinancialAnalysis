# we import the Twilio client from the dependency we just installed
from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
client = Client("AC9f438ba67912243c507e5b5310dbc846", "223fb1602b51981b52378c900d95974f")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to="+919880627826", from_="+14243733536", body="Hello from Python! -- FinTech")
