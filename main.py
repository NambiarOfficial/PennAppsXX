from flask import Flask, request, jsonify, Response, render_template
from flask_ask import Ask, question, statement
import requests
import json
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from twilio_test import send_msg


TEMP_FOLDER='./temp'
app = Flask('Alfred Pennyworth')
ask = Ask(app,'/alexa')
nodes = {'bathroom': '192.168.43.23'}
pi_ip = "http://192.168.43.138:5000"

@app.route('/test')
def test():
	return "Hello"

'''
ALEXA INTENTS
'''
@ask.launch
def alexa_welcome():
	'''
	Renders the welcome message on calling Alexa as 'Start Alfred Pennyworth'
	'''
	welcome = render_template('welcome')
	reprompt = render_template('reprompt')
	return question(welcome).reprompt(reprompt)

@ask.intent("AMAZON.YesIntent")
def test_yes():
	'''
	On calling any among Yes Intents
	'''
	return statement("Thats a yes from me")

@ask.intent("AMAZON.NoIntent")
def test_no():
	'''
	On calling No Intent
	'''
	return statement("Thats a no from me")

@ask.intent("SendTextIntent")
def send_text(text_name):
	send_msg('Hi')
	return statement("Message has been sent to "+name)

@ask.intent('NavigateIntent',mapping={'dest':'Location'})
def alexa_nav(dest):
	if dest is None:
		return question(render_template('reprompt'))
	print(dest)
	try:
		navigate(dest)
	except ConnectionError:
		return statement("Something seems to be taking time. Please wait or retry later")
	
	return statement('Went to room')

@ask.intent('LightIntent',mapping={'room':'Location','action':'Action'})
def alexa_light(room,action):
	if room is None or action is None:
		return question(render_template('reprompt'))
	print(room,action)
	home_automate(room,'light',action)
	return statement('Done')

@ask.intent('NewFaceIntent',mapping={'name':'name'})
def alexa_face_add(name):
	# TODO get name argument from alexa
	r = requests.get(pi_ip+'/add_new_face?name='+name)
	print(name)
	return name

@ask.intent('DetectFaceIntent')
def alexa_face_recog():
	req_id = request.json['request']['requestId'] #.replace('-','')
	print(req_id)
	api_access_token = request.json['context']['System']['apiAccessToken']
	api_endpoint = request.json['context']['System']['apiEndpoint']
	headers = {
	'Authorization':'Bearer ' + api_access_token,
	'Content-Type' : 'application/json'
	}
	data = { 
		"header":{ 
			"requestId":req_id
		},
		"directive":{ 
			"type":"VoicePlayer.Speak",
			"speech":"<speak>Please wait till we identify the person</speak>"
		}
	}
	r1 = requests.post(api_endpoint+'/v1/directives',headers=headers,data=data)
	print(r1)
	r = requests.get(pi_ip+'/face_detect')
	s = r.text
	print(s)
	return statement(s)

@ask.intent('DetectEventIntent')
def alexa_event_detect():
	r = requests.get(pi_ip+'/event')
	s = r.text
	print(s)
	return statement(s)

@ask.intent('DetectGeneralObjectIntent')
@ask.intent('DetectSpecificObjectIntent',mapping={'thing':'thing'})
def alexa_object_detect(thing=None):
	if thing is None:
		r = requests.get(pi_ip+'/object_detect')
	else:
		r = requests.get(pi_ip+'/object_detect?specific='+thing)
	return statement(r.text)

@ask.intent('DetectLandmarkIntent')
def alexa_landmark():
	r = requests.get(pi_ip+'/landmark')
	if r.text in ['None','none']:
		s = "I cannot see any famous landmarks around you"
	else:
		s = "You are looking at " + r.text
	return statement(s)

@ask.intent('ReadIntent')
def alexa_ocr():
	r = requests.get(pi_ip + '/ocr')
	print(r.text)
	return statement(r.text)

@ask.intent('HandwrittenIntent')
def alexa_ocr():
	r = requests.get(pi_ip+'/handwritten')
	return statement(r.text)
'''
END OF ALEXA STUFF
'''

@app.route('/node_reg',methods=['POST'])
def reg():
	node_id = request.form.get('id')
	ip = request.remote_addr
	nodes[node_id] = ip
	print(nodes)
	return '1'


'''
@app.route('/test',methods=['POST','GET'])
def test():
	l = int(request.args.get('length'))
	prev = int(request.args.get('prev'))
	r = random.randint(0,l-1)
	while r==prev:
		r = random.randint(0,l-1)
	d = {'val':r}
	return jsonify(d)

@app.route('/tts',methods=['POST'])
def tts():
	query = request.args.get('string') 
	speak(query)
	return 'TTS OK'

@app.route('/node_mcu_test',methods=['GET','POST'])
def node_mcu():
	print('Node MCU Data Received')
	print(request.remote_addr)
	return '1'

@app.route('/face',methods=['POST'])
def face():
	f = request.data
	img = cv2.imdecode(np.frombuffer(f,np.uint8), cv2.IMREAD_COLOR)
	face_detected,gray_img=fr.faceDetection(img)
	response = {}
	for face in face_detected:
		(x,y,w,h)=face
		roi_gray=gray_img[y:y+h,x:x+w]
		label,confidence=face_recognizer.predict(roi_gray)
		predicted_name=name[label]
		d = {'conf':confidence,'label':label}
		response[predicted_name] = d
	return jsonify(response)


@app.route('/face_recognition',methods=['POST'])
def face_recog():
	img_str = request.data
	img = cv2.imdecode(np.frombuffer(np.frombuffer(img_str, np.uint8),cv2.IMREAD_COLOR))
	face_detected,gray_img=fr.faceDetection(img)
	# print("faces detected:",len(face_detected))
	result_image,name=fr.image_label(face_detected,gray_img,face_recognizer,img)       
	# cv2.imshow('result',result_image)
	resp_str = 'Name is ' + name
	speak(resp_str)
	return resp_str

@app.route('/face_train',methods=['POST'])
def face_train():
	lists = os.listdir(os.path.join('Facial Recognition','train_image'))
	path_new=str(len(lists)-1)
	# cnf=int(input('Path_new is: '+path_new+'Are you sure you want to continue?'))
	cnf=1
	if cnf==1:
		registerer(path_new)
		faces,faceID=fr.labels_for_training_data(os.path.join(path1,path_new))
		face_recognizer=fr.train_classifier(faces,faceID)
		face_recognizer.save('trainingDataNew.yml')
		print('Data trained')
	else:
		print('Operation aborted!')
'''

@app.route('/',methods=['POST','GET'])
@app.route('/update',methods=['POST','GET'])
def gsm_test():
	temp = request.args.get('temperature')
	humid = request.args.get('humidity')
	lat = request.args.get('latitude')
	lon = request.args.get('longitude')
	print(request.remote_addr)
	print(temp,humid,lat,lon)
	return '1'

@app.route('/voice',methods=['POST'])
def voice():
	text = request.json['text']
	if len(text.split()) < 3: #Ignore partial results
		return '1'

	if 'navigate' in text or 'take me' in text:
		navigate(text.split('to')[-1][1:])

	elif 'turn' in text or 'switch' in text:
		args = text.split()
		print(args)
		home_automate(''.join(args[1:-2]),args[-2],args[-1]) 
	elif 'add new face' in text:
		args = text.split('add new face')[1]
		add_new_face(args)
	elif 'detect face' in text:
		detect_face()
	elif 'identify event' in text:
		event_detect()
	elif 'object detect' in text:
		object_detect()
	elif 'read text' in text:
		ocr()
	elif 'handwriting' in text:
		handwriting()
	elif 'text' in text:
		send_msg('hi')
	return '1'

def ocr():
	r = requests.get(pi_ip+'/ocr')

def handwriting():
	r = requests.get(pi_ip+'/handwriting')

def object_detect():
	r = requests.get(pi_ip+'/object_detect')

def event_detect():
	r = requests.get(pi_ip+'/event')
	print(r.text)

def detect_face():
	r = request.get(pi_ip+'/face_detect')
	print(r.json())

def navigate(destination):
	r = requests.get(pi_ip+'/navigate?dest='+destination)
	print(r)

def home_automate(room,device,action):
	ip = nodes[room]
	if action == 'on':
		r = requests.post('http://'+ip+':80/change',data='1')
		print(r)
	else:
		r = requests.post('http://'+ip+':80/change',data='0')
		print(r)

def add_new_face(args):
	r = requests.get(pi_ip+'/add_new_face?name='+args)
	print(r)

@app.route('/positions',methods=['POST'])
def positions():
	r = request.json
	print(r)
	plot(r)
	return '1'

def plot(pos):
	x = []
	y = []
	labels = []
	colors = ['red','blue','green','black']
	for i in pos.keys():
		x.append(pos[i]['x'])
		y.append(pos[i]['y'])
		labels.append(i)
	plots = []
	for i in range(len(x)):
		plots.append(plt.scatter([x[i]],[y[i]],c=colors[i],label=labels[i]))
	
	plt.legend()
	plt.savefig('./temp/pic.png')
	plt.clf()

if __name__ == '__main__':
	app.run(host='192.168.43.43',debug=True)
	# app.run(debug=True,port=5000)