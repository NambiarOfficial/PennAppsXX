from flask import Flask,request, jsonify
import rssi
import numpy as np
import RPi.GPIO as GPIO
# from face_detect import face_detect
from t2s import t2s
#from event_description import event_description
from face_recognise import match_faces, train_faces
from distance import get_ultrasonic
from ewma import ewma, wma
import json
import threading
#from googleAPI import detect_text, detect_landmarks, detect_document, detect_emotion, search_object
from azure_codes import object_detection, describe_image_local, landmark, handwriting_recognition, OCR_Recognition
import time
import requests
from twilio_test import send_msg
from transactions import create_transaction
from pyzbar.pyzbar import decode
import cv2

GPIO.setmode(GPIO.BOARD)
prev_time_nav = time.time()
count = 0
'''
	SET HAPTIC PINS
'''
haptic_pin_left = 35
haptic_pin_right = 32
frequency = 1

GPIO.setup(haptic_pin_left, GPIO.OUT)
GPIO.setup(haptic_pin_right, GPIO.OUT)
p_left = GPIO.PWM(haptic_pin_left,frequency)
p_right = GPIO.PWM(haptic_pin_right,frequency)
p_left.start(0)
p_right.start(0)
d_max = 15
cutoff_dist = 2
d_range = d_max-cutoff_dist
vib_max = 75
vib_min = 10
vib_range = vib_max-vib_min

'''
	END OF HAPTIC SETUP
'''

host_ip = '192.168.43.138'
app = Flask(__name__)
interface = 'wlan0'

name_dict = {'bathroom':'bathroom','bedroom':'bathroom1','kitchen':'bathroom2'}
inp1 = {'bathroom1':{
		'signalAttenuation': 3, 
		'location': {
				'y': 15, 
				'x': 0
		}, 
		'reference': {
				'distance': 4, 
				'signal': -50
		}, 
		'name': 'bathroom1'
}
,'bathroom':{
		'signalAttenuation': 3, 
		'location': {
				'y': 0, 
				'x': 30
		}, 
		'reference': {
				'distance': 4, 
				'signal': -50
		}, 
		'name': 'bathroom'
},'bathroom2':{
		'signalAttenuation': 3, 
		'location': {
				'y': 30, 
				'x': 15
		}, 
		'reference': {
				'distance': 4, 
				'signal': -50
		}, 
		'name': 'bathroom2'
}}

inp = list(inp1.values())
pos_dict = {}
for i in inp1.keys():
	pos_dict[i] = inp1[i]['location']

def cleanup():
	GPIO.cleanup()

def weighted_avg(d,d1):
	if d == d_max:
		d = d1
	else:
		d = d*0.3 + d1*0.7
	return d

def vibrate(d, direction='straight'):
	global p_left, p_right
	global count
	global prev_time_nav
	d = cutoff_dist if d<cutoff_dist else d
	d = d_max if d>d_max else d
	if time.time() - prev_time_nav > 1:
		# if direction == 'straight':
		s = str(int(d))
		prev_time_nav = time.time()
		# else:
			# s = str(int(d))+' '+direction
		#t1 = threading.Thread(target=t2s,args=(s,))
		#t1.start()
	vib = -(d-cutoff_dist)*(vib_range)/d_range+vib_max
	# print(vib)
	if direction == 'left':
		p_right.ChangeDutyCycle(0)
		p_left.ChangeDutyCycle(vib)
	elif direction == 'right':
		p_left.ChangeDutyCycle(0)
		p_right.ChangeDutyCycle(vib)
	else:
		p_left.ChangeDutyCycle(vib)
		p_right.ChangeDutyCycle(vib)

@app.route('/navigate')
def navigate():
	global p_left, p_right
	signals = []
	dest = request.args.get('dest')
	r1 = rssi.RSSI_Scan(interface)
	r2 = rssi.RSSI_Localizer(inp)
	networks = [name_dict[str(dest)]]
	# print(networks)
	d = d_max
	p_left.ChangeDutyCycle(0)
	p_right.ChangeDutyCycle(0)
	vibrate(10,'straight')
	while d>cutoff_dist:
		'''
		plot_signals = []
		try:
			sig = r1.getAPinfo(sudo=True,networks=list(name_dict.values()))
		except:
			print("Cannot get the network")
			continue
		for i in sig:
			if i['ssid'] == networks[0]:
				signals.append(i['signal'])
			#plot_signals.append(i['signal'])
		print(sig)
		#print('Plot signals',plot_signals)
		if len(signals) < 5:
			continue
		pos = r2.getNodePosition(plot_signals)
		pos_dict['node'] = {}
		pos_dict['node']['x'] = float(pos[0])
		pos_dict['node']['y'] = float(pos[1])
		print(pos_dict)
		#requests.post('http://192.168.43.43:5000/positions',json=pos_dict)
		# d = weighted_avg(d,d1)
		# dist.append(d1)
		signals = signals[-5:]
		# sig = wma(signals)
		d = r2.getDistanceFromAP(inp1[name_dict[str(dest)]],signals[-1])['distance']
		#print('Sig,d',sig,d)

		direction_array = get_ultrasonic()
		if direction_array is None:
			direction = 'straight'
		elif direction_array[0] == 0:
			direction = 'left'
		elif direction_array[1] == 0:
			direction = 'straight'
		else:
			direction = 'right'
		'''
		#direction = 'straight'
		#print(direction)
		#vibrate(d,direction)
		time.sleep(0.001)
		t1 = threading.Thread(target=t2s,args=('Right',))
		t1.start()
		break
	time.sleep(3.5)
	# vibrate(d)
	p_left.ChangeDutyCycle(0)
	p_right.ChangeDutyCycle(0)
	print('You have reached your destination')
	t1 = threading.Thread(target=t2s,args=('You have reached your destination',))
	t1.start()
	return '1'

@app.route('/add_new_face',methods=['GET','POST'])
def add_new_face():
	name = request.args.get('name')
	train_faces(name)
	print("Done adding face")
	t1 = threading.Thread(target=t2s,args=('Done adding face',))
	t1.start()
	return '1'

@app.route('/face_detect')
def face_detect_pi():
	names = {'names':[]}
	names['names'],l = match_faces()
	# print(n)
	#names = face_detect()
	if len(names['names']) == 0:
		s = "I can't seem to find anyone in front of you"
	elif len(names['names']) == 1:
		s = "I have found " + names['names'][0]+ " in front of you."
		print(names['names'][0])
		#emo = emotion()
		#print(emo)
		#s += (" They seem to be " + emo[0])
	else:
		s = "I have found " + ",".join(names['names']) + " in front of you"
	print(s)
	t1 = threading.Thread(target=t2s, args=(s,))
	t1.start()
	return s
	# return names

@app.route('/emotion')
def emotion():
	emo = detect_emotion()
	return emo

@app.route('/event')
def event():
	#event_des = event_description()
	event_des = describe_image_local()
	event_des = sorted(event_des,key=lambda caption:caption.confidence)[-1].text
	print(event_des)
	if 'fire' in event_des or 'smok' in event_des:
		send_sos()
	t1 = threading.Thread(target=t2s, args=(event_des,))
	t1.start()
	return event_des

@app.route('/object_detect')
def object_detect():
	thing = request.args.get('specific')
	if thing is None:
		#items = search_object()
		items = object_detection()
		items = [item.object_property for item in items]
		s = "You are looking at " + ','.join(items)
	else:
		s = object_detection(thing)
		#s = "You should find " + thing + "on the " + loc
	print(s)
	t1 = threading.Thread(target=t2s, args=(s,))
	t1.start()
	return s


@app.route('/landmark')
def landmark():
	#landmarks = set(detect_landmarks())
	landmarks = set(l['name'] for l in landmark())
	s = ','.join(landmarks)
	s1 = "You are looking at "+s
	t1 = threading.Thread(target=t2s, args=(s1,))
	t1.start()
	return s

@app.route('/ocr')
def ocr():
	#text = detect_text()
	text = OCR_Recognition()
	print(text)
	t1 = threading.Thread(target=t2s, args=(text,))
	t1.start()
	return text

@app.route('/handwritten')
def handwritten():
	#text = detect_document()
	text = handwriting_detection()
	t1 = threading.Thread(target=t2s, args=(text,))
	t1.start()
	return text

def home_automate(room,device,action):
	ip = nodes[room]
	if action == 'on':
		r = requests.post('http://'+ip+':80/change',data='1')
		print(r)
	else:
		r = requests.post('http://'+ip+':80/change',data='0')
		print(r)

def object_detect_pi():
	#items = search_object()
	items = object_detection()
	items = [item.object_property for item in items]
	s = "You are looking at " + ','.join(items)
	print(s)
	t1 = threading.Thread(target=t2s, args=(s,))
	t1.start()
	return s

def send_sos():
	send_msg("SOS! Send help to my location - (39.951681, -75.191207)")
	t2s("Emergency services have been alerted and are on their way. Remain calm.")

@app.route('/payment')
def payment():
	cap = cv2.VideoCapture(0)
	_. frame = cap.read()
	cap.release()
	data = decode(frame).data.decode('utf-8')
	receiver,amount = data.spilt(',')
	create_transaction('Spidey',receiver,amount,'Payment made to merchant')
	s = 'Payment of '+amount+' made to '+receiver
	t1 = threading.Thread(target=t2s,args=(s,))
	t1.start()
	return '1'
'''
	SET PUSH BUTTON PINS AND CALLBACKS
'''
curr_mode = -1

pb_up_pin = 36
pb_down_pin = 37
modes = {
	0:['Detect Face',face_detect_pi],
	1:['Read Text',ocr],
	2:['Event Description',event],
	3:['Object Detect',object_detect_pi],
	4:['Send SOS',send_sos],
	5:['Pay merchant', payment]
	}
num_modes = len(modes.keys())
def counter_callback(channel):
	global curr_mode
	start_time  = time.time()
	while GPIO.input(channel) == 0:
		pass
	
	time_diff = time.time() - start_time
	if time_diff>0.5:
		print('calling function')
		modes[curr_mode][1]()
	elif time_diff>0.05:
		if channel == pb_up_pin:
			curr_mode = (curr_mode+1)%num_modes
		elif channel == pb_down_pin:
			curr_mode = (curr_mode-1)%num_modes
		print('In callback with mode '+str(curr_mode))
		s = 'Current mode is ' + modes[curr_mode][0] +'. Long press to confirm'
		t2s(s)
	

GPIO.setup(pb_up_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(pb_down_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pb_up_pin,GPIO.FALLING,callback=counter_callback,bouncetime=200)
GPIO.add_event_detect(pb_down_pin,GPIO.FALLING,callback=counter_callback,bouncetime=200)

'''
	END OF PUSH BUTTON SETUP
'''

if __name__ == '__main__':
	try:
		app.run(host=host_ip)
	finally:
		print('Cleaning up')
		p_left.stop()
		p_right.stop()
		# GPIO.cleanup()
