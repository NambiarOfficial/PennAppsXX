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
 
account_sid = 'AC57bc9b762fce7d203cc00ccd765cbe7f' 
auth_token = '171356b0d99c9bf3b1fb57498803d919' 
client = Client(account_sid, auth_token) 
# text = input("What is the message?\n")

def send_msg(text):
	message = client.messages.create( 
								from_='+12053031167',  
								body=text,      
								to='+16318292196'
							) 
 
	print(message.sid)