from azure_functions import object_detection, describe_image, handwriting_recognition, OCR_Recognition
from new_face_recognise import train_faces, match_faces
from random import choice
import cv2

default_images = ['test_pic.jpg']

def take_image():
    cap = cv2.VideoCapture(0)
    _, capture = cap.read()
    cap.release()
    cv2.imwrite('azure.jpg',capture)
    print('Pic taken')

functions = {1:object_detection,
	3:describe_image,
	4:OCR_Recognition,
	6:match_faces}

while True:
	print('What feature would you like to demo?')
	opt = int(input('1. Detect all objects in frame\n2. Detect a specific object\n3. Describe an image\n4. Read text\n5. Add new face\n6. Identify Face\nEnter option : '))
	own_image = input('Do you want to use the webcam or use a default image? (1 - Webcam, 2 - Default) : ')
	filename = 'azure.jpg'
	if own_image == '1':
		take_image()
	else:
		filename = choice(default_images)

	if opt == 2:
		obj = input('What object do you want to see? : ').lower()
		object_detection(filename,obj)
	elif opt == 5:
		name = input('Who is this user?')
		train_faces(image,name)
	else:
		functions[opt](filename)

	if(input("Do you wish to continue? (Y/N)").lower() == 'n'):
		break
