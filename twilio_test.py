# from twilio.rest import Client

# account_sid = 'SK243b332195e294174a62503c06830d1b' 
# auth_token = 'OCnfGrKkhYRJ2CEpxWl42taZCrZI0EkK'
# client = Client(account_sid, auth_token)
# message = client.messages.create(
# 							from_='+12053031167',
# 							body='Hi there!',
# 							to='+16318292196'
#                           )

# print(message.sid)

from twilio.rest import Client
from credentials import account_sid, auth_token
 
client = Client(account_sid, auth_token) 
# text = input("What is the message?\n")

def send_msg(text):
	message = client.messages.create( 
								from_='+12053031167',  
								body=text,      
								to='+919655558174'
							) 
 
	print(message.sid)


if __name__ == '__main__':
	text = input("Whats the message?")
	send_msg(text)