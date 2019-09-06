import cv2
import requests
subscription_key = '99777c636bdd49f081b97aafb239fa8e'
assert subscription_key
_region = 'southeastasia' #Here you enter the region of your subscription
analyze_url = 'http://{}.api.cognitive.microsoft.com/vision/v2.0/analyze'.format(_region)

def event_description():
	cap = cv2.VideoCapture(0)
	_, image = cap.read()
	_,enc=cv2.imencode('.jpg',image)
	image_data=enc.tobytes()
	headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           	'Content-Type': 'application/octet-stream'}
	params = {'visualFeatures': 'Categories,Description,Color'}
	response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
	response.raise_for_status()
	analysis = response.json()
	image_caption = analysis["description"]["captions"][0]["text"].capitalize()
	return (image_caption)

