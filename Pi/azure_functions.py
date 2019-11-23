from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import os
import sys
import time
import cv2
import numpy as np

threshold_accuracy=0.4
font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 0.5
fontColor              = (0,0,0)
lineType               = 2

remote_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"

endpoint = "https://penappsxx.cognitiveservices.azure.com/"
subscription_key = '99777c636bdd49f081b97aafb239fa8e'
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def describe_image(filename):
	local_image = open(filename,'rb')
	description_result = computervision_client.describe_image_in_stream(local_image)
	local_image.close()
	if (len(description_result.captions) == 0):
		print("No description detected.")
	else:
		caption = sorted(description_result.captions,key= lambda i: i.confidence)[-1]
		print(caption.text)

def object_detection(filename,thing=None):
	local_image = open(filename,'rb') #as local_image:
	detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image)
	local_image.close()
	if len(detect_objects_results_local.objects) == 0:
		print("No objects detected.")
	elif thing is None:
		items = [item.object_property for item in detect_objects_results_local.objects]
		print('Found ' + ','.join(items))
	else:
		res = "Could not find object"
		for objectsd in detect_objects_results_local.objects:
			if objectsd.object_property.lower() == thing:
				cx =  int((objectsd.rectangle.x + objectsd.rectangle.x + objectsd.rectangle.w)/2)
				cy =  int((objectsd.rectangle.y + objectsd.rectangle.y + objectsd.rectangle.h)/2)
				found = [[thing,[cx,cy]]]
				res = "Object was found in " + locate(found)[0][1]
		print(res)

def locate(found):
	image = cv2.imread(filename)
	x = np.shape(image)[1]
	y = np.shape(image)[0]

	labels=['Top Right','Top Left','Bottom Right','Bottom Left','At the Center','Not sure if it is the same object']
	final=[]
	for objects in found:
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
	return(final)

def object_detection(filename):
	local_image = open(filename,'rb') #as local_image:
	detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image)
	local_image.close()
	if len(detect_objects_results_local.objects) == 0:
		print("No objects detected.")
	else:
		items = [item.object_property for item in detect_objects_results_local.objects]
		print('Found ' + ','.join(items))

def handwriting_recognition(filename):
	local_image = open(filename,'rb') #as local_image:
	recognize_handwriting_results = computervision_client.batch_read_file_in_stream(local_image, raw=True)
	local_image.close()
	operation_location_local = recognize_handwriting_results.headers["Operation-Location"]
	operation_id_local = operation_location_local.split("/")[-1]
	while True:
		recognize_handwriting_result = computervision_client.get_read_operation_result(operation_id_local)
		if recognize_handwriting_result.status not in ['NotStarted', 'Running']:
			break
		time.sleep(1)
	s=''
	if recognize_handwriting_result.status == TextOperationStatusCodes.succeeded:
		for text_result in recognize_handwriting_result.recognition_results:
			for line in text_result.lines:
				s+=(line.text+' ')
				print(line.text)
				print(line.bounding_box)
	print(s)

def OCR_Recognition(filename):
	local_image = open(local_image_path,'rb') #as local_image:
	ocr_result_local = computervision_client.recognize_printed_text_in_stream(local_image)
	local_image.close()
	s=''
	for region in ocr_result_local.regions:
		for line in region.lines:
			print("Bounding box: {}".format(line.bounding_box))
			s += "\n"
			for word in line.words:
				s += word.text + " "
			print(s)
	return s

def OCR_Recognition_url(url):
	ocr_result_local = computervision_client.recognize_printed_text(url)
	for region in ocr_result_local.regions:
		for line in region.lines:
			print("Bounding box: {}".format(line.bounding_box))
			s = ""
			for word in line.words:
				s += word.text + " "
			print(s)


if __name__ == '__main__':
	print([i.text for i in describe_image_local()])
