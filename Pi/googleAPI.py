#Google Labels Code
import io
import os
from google.cloud import vision
from google.cloud.vision import types
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='My First Project-88f25c3d63b5.json'
client=vision.ImageAnnotatorClient()

def get_image():
	cap = cv2.VideoCapture(0)
	_, content = cap.read()
	cap.release()
	content = cv2.flip(content,-1)
	_,image=cv2.imencode('.jpg',content)
	image=image.tobytes()
	image = vision.types.Image(content=image)
	return image

def detect_text():
	image = get_image()
	response = client.text_detection(image=image)
	texts = response.text_annotations
	return texts[0].description

def detect_labels():
	image = get_image()
	all_descriptor=[]

	response = client.label_detection(image=image)
	labels = response.label_annotations
	all_descriptor = [[label.description,label.score] for label in labels]
	return(all_descriptor)

def detect_landmarks():
	image = get_image()
	landmark_descriptor=[]
	response = client.landmark_detection(image=image)
	landmarks = response.landmark_annotations
	landmark_descriptor = [landmark.description for landmark in landmarks]
	return(landmark_descriptor)

def detect_brand_shops():
	image = get_image()
	brand_shops=[]
	response = client.logo_detection(image=image)
	logos = response.logo_annotations
	brand_shops = [[logo.description,logo.score] for logo in logos]
	return(brand_shops)

def detect_document():
	image = get_image()

	symbols=''
	response = client.document_text_detection(image=image)

	for page in response.full_text_annotation.pages:
		for block in page.blocks:
			for paragraph in block.paragraphs:
				for word in paragraph.words:
					for symbol in word.symbols:
						symbols+=symbol.text
					symbols+=' '
		return(symbols)

def detect_emotion():
	image = get_image()
	response = client.face_detection(image=image)
	faces = response.face_annotations
	print(len(faces))
	# Names of likelihood from google.cloud.vision.enums
	likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
					   'LIKELY', 'VERY_LIKELY')
	# print('Faces:')
	emotion=['Angry','Joy','Surprise']
	count=0
	texts=[]
	for face in faces:
		vertices = (['({},{})'.format(vertex.x, vertex.y)
					for vertex in face.bounding_poly.vertices])
		emotion_meter=[face.anger_likelihood,face.joy_likelihood,face.surprise_likelihood]
		texts.append(emotion[emotion_meter.index(max(emotion_meter))])
	return(texts)

def search_object(thing=None):
	cap = cv2.VideoCapture(0)
	_, content = cap.read()
	cap.release()
	found=[]
	content = cv2.flip(content,-1)
	#centroid=[]
	y,x=np.shape(content)[:2]
	# disp=content.copy()
	_,image=cv2.imencode('.jpg',content)
	image=image.tobytes()
	image = vision.types.Image(content=image)
	objects = client.object_localization(image=image).localized_object_annotations
	# total_objects=len(objects)
	if thing is None:
		items = [item.name for item in objects]
		return items
	for object_ in objects:
		print('In object loop ', object_.name)
		if object_.name.lower() == thing:
			pt1=(int(x*object_.bounding_poly.normalized_vertices[0].x),int(y*object_.bounding_poly.normalized_vertices[0].y))
			pt2=(int(x*object_.bounding_poly.normalized_vertices[2].x),int(y*object_.bounding_poly.normalized_vertices[2].y))
			tempCx=int((pt1[0]+pt2[0])/2)
			tempCy=int((pt1[1]+pt2[1])/2)
			found.append([object_.name,[tempCx,tempCy],object_.score,[x,y]])
			location = locate(found)
			break
	return(location[0][1])

def locate(found):
	labels=['Top Right','Top Left','Bottom Right','Bottom Left','At the Center','Not sure if it is the same object']
	x,y=found[0][3]
	final=[]
	for objects in found:
		if objects[2]>0.7:
			if (objects[1][0]>=0 and objects[1][0]<=int(x/2) and objects[1][1]>=0 and objects[1][1]<=int(y/2)):
				final.append([objects,labels[1]])
			elif (objects[1][0]>=int(x/2) and objects[1][0]<=x and objects[1][1]>=0 and objects[1][1]<=int(y/2)):
				final.append([objects,labels[0]])
			elif (objects[1][0]>=0 and objects[1][0]<=int(x/2) and objects[1][1]>=int(y/2) and objects[1][1]<=y):
				final.append([objects,labels[3]])
			elif (objects[1][0]>=int(x/2) and objects[1][0]<=x and objects[1][1]>=int(y/2) and objects[1][1]<=y):
				final.append([objects,labels[2]])
			if (objects[1][0]>=int(7*x/9) and objects[1][0]<=int(11*x/9) and objects[1][1]>=int(7*x/9) and objects[1][1]<=int(11*x/9)):
				final.append([objects,labels[4]])
		else:
			final.append([objects,labels[5]])
	return(final)