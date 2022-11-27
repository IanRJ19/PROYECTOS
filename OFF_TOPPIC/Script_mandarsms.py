# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from decouple import config


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid =config("CUENTA_TWILIO")
auth_token =config("CONTRA_TWILIO")
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Hola mundo",
                     from_='+12183069958',
                     to='+51993343179'
                 )

print(message.sid)


print("all good")
