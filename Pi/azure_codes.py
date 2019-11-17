from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure_credentials import subscription_key

import os
import sys
import time
import cv2
import numpy as np
#Custom variables
#Github repo: https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/python/ComputerVision/ComputerVisionQuickstart.py
threshold_accuracy=0.4
font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 0.5
fontColor              = (0,0,0)
lineType               = 2

local_image_path = "/home/pi/PennAppsXX/Pi/azure_pic.jpg"
remote_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg"

endpoint = "https://penappsxx.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
#local_image = open(local_image_path, "rb")
#imageface=cv2.imread(local_image_path)
#_,enc=cv2.imencode('.jpg',imageface)
#image_data = enc.tobytes()

def get_image():
    cap = cv2.VideoCapture(0)
    _, capture = cap.read()
    cap.release()
    #capture = cv2.flip(capture,-1)
    cv2.imwrite(local_image_path,capture)
    print('Pic taken')

def describe_image_local():
    get_image()
    local_image = open(local_image_path,'rb') #as local_image:
    description_result = computervision_client.describe_image_in_stream(local_image)
    local_image.close()
    #print("Description of local image: ")
    if (len(description_result.captions) == 0):
        print("No description detected.")
    else:
        return description_result.captions
        for caption in description_result.captions:
            print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
# describe_image_local()
def describe_image_remote(remote_image_url):
    description_results = computervision_client.describe_image(remote_image_url )
    #print("Description of remote image: ")
    if (len(description_results.captions) == 0):
        print("No description detected.")
    else:
        for caption in description_results.captions:
            print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))

def categorize_image():
    local_image_features = ["categories"]
    categorize_results_local = computervision_client.analyze_image_in_stream(local_image, local_image_features)
    #print("Categories from local image: ")
    if (len(categorize_results_local.categories) == 0):
        print("No categories detected.")
    else:
        for category in categorize_results_local.categories:
            print("'{}' with confidence {:.2f}%".format(category.name, category.score * 100))

def categorize_image_remote(image_url):
    local_image_features = ["categories"]
    categorize_results_remote = computervision_client.analyze_image(image_url , local_image_features)
    #print("Categories from local image: ")
    if (len(categorize_results_local.categories) == 0):
        print("No categories detected.")
    else:
        for category in categorize_results_local.categories:
            print("'{}' with confidence {:.2f}%".format(category.name, category.score * 100))

def tags_of_image():
    tags_result_local = computervision_client.tag_image_in_stream(local_image)
    #print("Tags in the local image: ")
    if (len(tags_result_local.tags) == 0):
        print("No tags detected.")
    else:
        for tag in tags_result_local.tags:
            print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))

def tags_of_image_remote(remote_image_url):
    tags_result_remote = computervision_client.tag_image(remote_image_url )
    #print("Tags in the remote image: ")
    if (len(tags_result_remote.tags) == 0):
        print("No tags detected.")
    else:
        for tag in tags_result_remote.tags:
            print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))

def detect_faces_and_ages():
    local_image_features = ["faces"]
    detect_faces_results_local = computervision_client.analyze_image_in_stream(local_image, local_image_features)
    print("Faces in the local image: ")
    if (len(detect_faces_results_local.faces) == 0):
        print("No faces detected.")
    else:
        detected_image=imageface.copy()
        for face in detect_faces_results_local.faces:
            x1=int(face.face_rectangle.top)
            x2=int(face.face_rectangle.top+face.face_rectangle.height)
            y1=int(face.face_rectangle.left)
            y2=int(face.face_rectangle.left+face.face_rectangle.width)
            cv2.rectangle(detected_image,(y1,x1),(y2,x2),(0,255,255),2)
            cv2.rectangle(detected_image,(y1,x1-30),(y1+100,x1),(0,255,255),cv2.FILLED)
            cv2.putText(detected_image,'Age: '+str(face.age), (y1+10,x1-10) ,font, fontScale,fontColor,lineType)
            print("'{}' of age {} at location {}, {}, {}, {}".format(face.gender, face.age, \
            face.face_rectangle.left, face.face_rectangle.top, \
            face.face_rectangle.left + face.face_rectangle.width, \
            face.face_rectangle.top + face.face_rectangle.height))
    cv2.imshow("Detected",detected_image)

def detect_faces_and_ages_url(remote_url_faces):
    remote_url_features = ["faces"]
    detect_faces_results_remote = computervision_client.analyze_image(remote_url_faces, remote_url_features)
    print("Faces in the local image: ")
    if (len(detect_faces_results_local.faces) == 0):
        print("No faces detected.")
    else:
        for face in detect_faces_results_local.faces:
            print("'{}' of age {} at location {}, {}, {}, {}".format(face.gender, face.age, \
            face.face_rectangle.left, face.face_rectangle.top, \
            face.face_rectangle.left + face.face_rectangle.width, \
            face.face_rectangle.top + face.face_rectangle.height))

def adult_and_racy_content():
    local_image_features = ["adult"]
    detect_adult_results_local = computervision_client.analyze_image_in_stream(local_image, local_image_features)
    print("Is adult content: {} with confidence {:.2f}".format(detect_adult_results_local .adult.is_adult_content, detect_adult_results_local .adult.adult_score * 100))
    print("Has racy content: {} with confidence {:.2f}".format(detect_adult_results_local .adult.is_racy_content, detect_adult_results_local .adult.racy_score * 100))

def adult_and_racy_content_url():
    remote_image_features = ["adult"]
    detect_adult_results_remote = computervision_client.analyze_image(remote_image_url, remote_image_features)
    print("Is adult content: {} with confidence {:.2f}".format(detect_adult_results_local .adult.is_adult_content, detect_adult_results_local .adult.adult_score * 100))
    print("Has racy content: {} with confidence {:.2f}".format(detect_adult_results_local .adult.is_racy_content, detect_adult_results_local .adult.racy_score * 100))

def color_scheme():
    local_image_features = ["color"]
    detect_color_results_local = computervision_client.analyze_image_in_stream(local_image, local_image_features)
    print("Is black and white: {}".format(detect_color_results_local.color.is_bw_img))
    print("Accent color: {}".format(detect_color_results_local.color.accent_color))
    print("Dominant background color: {}".format(detect_color_results_local.color.dominant_color_background))
    print("Dominant foreground color: {}".format(detect_color_results_local.color.dominant_color_foreground))
    print("Dominant colors: {}".format(detect_color_results_local.color.dominant_colors))

def color_scheme_url(url):
    local_image_features = ["color"]
    detect_color_results_local = computervision_client.analyze_image(image_url, local_image_features)
    print("Is black and white: {}".format(detect_color_results_local.color.is_bw_img))
    print("Accent color: {}".format(detect_color_results_local.color.accent_color))
    print("Dominant background color: {}".format(detect_color_results_local.color.dominant_color_background))
    print("Dominant foreground color: {}".format(detect_color_results_local.color.dominant_color_foreground))
    print("Dominant colors: {}".format(detect_color_results_local.color.dominant_colors))

def celebrity():
    detect_domain_results_celebs_local = computervision_client.analyze_image_by_domain_in_stream("celebrities", local_image)
    if len(detect_domain_results_celebs_local.result["celebrities"]) == 0:
        print("No celebrities detected.")
    else:
        for celeb in detect_domain_results_celebs_local.result["celebrities"]:
            print(celeb["name"])
def landmark():
    get_image()
    local_image = open(local_image_path,'rb') #as local_image:
    detect_domain_results_landmark_local = computervision_client.analyze_image_by_domain_in_stream("landmarks", local_image)
    local_image.close()
    if len(detect_domain_results_landmark_local.result["landmarks"]) == 0:
        print("No landmarks detected.")
    else:
        return detect_domain_results_landmark_local.result['landmarks']
        for landmark in detect_domain_results_landmark_local.result["landmarks"]:
            print(landmark["name"])

def celebrity_url(image_url):
    detect_domain_results_celebs_local = computervision_client.analyze_image_by_domain("celebrities", image_url)
    if len(detect_domain_results_celebs_local.result["celebrities"]) == 0:
        print("No celebrities detected.")
    else:
        for celeb in detect_domain_results_celebs_local.result["celebrities"]:
            print(celeb["name"])

def landmark_url(image_url):
    detect_domain_results_landmark_local = computervision_client.analyze_image_by_domain("landmarks", image_url)
    if len(detect_domain_results_landmark_local.result["landmarks"]) == 0:
        print("No landmarks detected.")
    else:
        for landmark in detect_domain_results_landmark_local.result["landmarks"]:
            print(landmark["name"])

def image_types():
    local_image_features = VisualFeatureTypes.image_type
    detect_type_results_local = computervision_client.analyze_image_in_stream(local_image, local_image_features)
    if detect_type_results_local.image_type.clip_art_type == 0:
        print("Image is not clip art.")
    elif detect_type_results_local.image_type.line_drawing_type == 1:
        print("Image is ambiguously clip art.")
    elif detect_type_results_local.image_type.line_drawing_type == 2:
        print("Image is normal clip art.")
    else:
        print("Image is good clip art.")

    if detect_type_results_local.image_type.line_drawing_type == 0:
        print("Image is not a line drawing.")
    else:
        print("Image is a line drawing")

def image_types_url(url):
    local_image_features = VisualFeatureTypes.image_type
    detect_type_results_local = computervision_client.analyze_image(url, local_image_features)
    if detect_type_results_local.image_type.clip_art_type == 0:
        print("Image is not clip art.")
    elif detect_type_results_local.image_type.line_drawing_type == 1:
        print("Image is ambiguously clip art.")
    elif detect_type_results_local.image_type.line_drawing_type == 2:
        print("Image is normal clip art.")
    else:
        print("Image is good clip art.")

    if detect_type_results_local.image_type.line_drawing_type == 0:
        print("Image is not a line drawing.")
    else:
        print("Image is a line drawing")

def object_detection():
    get_image()
    local_image = open(local_image_path,'rb') #as local_image:
    detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image)
    local_image.close()
    if len(detect_objects_results_local.objects) == 0:
        print("No objects detected.")
    else:
        return detect_objects_results_local.objects
        for objectsd in detect_objects_results_local.objects:
            print(objectsd.object_property)
            print("object at location {}, {}, {}, {}".format( \
            objectsd.rectangle.x, objectsd.rectangle.x + objectsd.rectangle.w, \
            objectsd.rectangle.y, objectsd.rectangle.y + objectsd.rectangle.h))

def object_detection_url():
    detect_objects_results_local = computervision_client.detect_objects(url)
    if len(detect_objects_results_local.objects) == 0:
        print("No objects detected.")
    else:
        for objectsd in detect_objects_results_local.objects:
            print(objectsd.object_property)
            print("object at location {}, {}, {}, {}".format( \
            objectsd.rectangle.x, objectsd.rectangle.x + objectsd.rectangle.w, \
            objectsd.rectangle.y, objectsd.rectangle.y + objectsd.rectangle.h))

def brands_available():
    local_image_features = ["brands"]
    detect_brands_results_local = computervision_client.analyze_image_in_stream(local_image, local_image_features)
    if len(detect_brands_results_local.brands) == 0:
        print("No brands detected.")
    else:
        for brand in detect_brands_results_local.brands:
            print("'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format( \
            brand.name, brand.confidence * 100, brand.rectangle.x, brand.rectangle.x + brand.rectangle.w, \
            brand.rectangle.y, brand.rectangle.y + brand.rectangle.h))

def brands_available_url(url):
    local_image_features = ["brands"]
    detect_brands_results_local = computervision_client.analyze_image(url, local_image_features)
    if len(detect_brands_results_local.brands) == 0:
        print("No brands detected.")
    else:
        for brand in detect_brands_results_local.brands:
            print("'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format( \
            brand.name, brand.confidence * 100, brand.rectangle.x, brand.rectangle.x + brand.rectangle.w, \
            brand.rectangle.y, brand.rectangle.y + brand.rectangle.h))

def handwriting_recognition():
    get_image()
    local_image = open(local_image_path,'rb') #as local_image:
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
    return s

def handwriting_recognition_url(url):
    recognize_handwriting_results = computervision_client.batch_read_file(url, raw=True)
    operation_location_local = recognize_handwriting_results.headers["Operation-Location"]
    operation_id_local = operation_location_local.split("/")[-1]
    while True:
        recognize_handwriting_result = computervision_client.get_read_operation_result(operation_id_local)
        if recognize_handwriting_result.status not in ['NotStarted', 'Running']:
            break
        time.sleep(1)
    if recognize_handwriting_result.status == TextOperationStatusCodes.succeeded:
        for text_result in recognize_handwriting_result.recognition_results:
            for line in text_result.lines:
                print(line.text)
                print(line.bounding_box)

def OCR_Recognition():
    get_image()
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
