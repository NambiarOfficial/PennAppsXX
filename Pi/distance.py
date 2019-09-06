import RPi.GPIO as GPIO
import time
import cv2
import numpy as np

GPIO.setmode(GPIO.BOARD)
TRIG=7
ECHO=12
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

adaptive_filter=100
direction1=[1,1,1]
direction=[0,0,0]

def Distance():
	GPIO.output(TRIG,0)
	time.sleep(0.1)
	GPIO.output(TRIG,True)
	time.sleep(0.00001)
	GPIO.output(TRIG,False)
	timeout=time.time()
	while GPIO.input(ECHO)==0:
		if abs(timeout-time.time())>1:
			return 
			break
	start=time.time()
	while GPIO.input(ECHO)==1:
		pass
	stop=time.time()
	return((stop-start)*17000)


def Distance_Predict(frame):
	y,x=np.shape(frame)[:2]
	ROI_frame=frame[int(5*y/8):y,:]
	frame=cv2.GaussianBlur(ROI_frame,(7,7),0)
	col=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	_,thresh=cv2.threshold(col,100,255,cv2.THRESH_BINARY_INV)
	ROI_extract1=thresh[:,0:int(x/3)]
	ROI_extract2=thresh[:,int(x/3):int(2*x/3)]
	ROI_extract3=thresh[:,int(2*x/3):x]
	direction[0],direction[1],direction[2]=(cv2.countNonZero(ROI_extract1),cv2.countNonZero(ROI_extract2),cv2.countNonZero(ROI_extract3))
	direction1=[1,1,1]
	direction1[direction.index(min(direction))]=0
	return(direction1)

def get_ultrasonic():
	dist=Distance()
	print(dist)
	if dist<=60:
		cam = cv2.VideoCapture(0)
		_,frame=cam.read()
		frame = cv2.flip(frame,1)
		direction_array=Distance_Predict(frame)
		# print(direction_array)
		cam.release()
		return direction_array

if __name__ == '__main__':
	while True:
		d = get_ultrasonic()
		print(d)