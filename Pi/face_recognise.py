import face_recognition
from PIL import Image, ImageDraw
import cv2
import numpy as np
import pickle
text=cv2.FONT_HERSHEY_TRIPLEX
known_face_names = ["Shivam","Harshit","Anant"]
#########DEK BHAI PI ME MOUNT KRE TO FLIPPING ENABLE KRNA PAKKA SEEEEEEEEEEEEEEEEEEEEEEEE@##############################
##########Dono Functions me#################

def match_faces():
    with open('Encodings.pkl','rb') as f:
        known_face_encodings = pickle.load(f)
    with open('Names.pkl','rb') as f:
        known_face_names = pickle.load(f)
    facesfound=[]
    cam=cv2.VideoCapture(0)
    _,test_image=cam.read()
    test_image=cv2.flip(test_image,-1)
    #thr=test_image.copy()
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)
    for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
      matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
      name = "Unknown Person"
      if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
      #thr=cv2.rectangle(thr.copy(),(left,top),(right,bottom),(0,255,255),2)
      #thr=cv2.rectangle(thr.copy(),(left,top-10),(right,top),(0,255,255),cv2.FILLED)
      #thr=cv2.putText(thr.copy(),name,(left+10,top-2),text,0.5,(0,0,0),lineType=cv2.LINE_AA)
      facesfound.append(name)
      #cv2.imwrite("faces_detected.jpg",thr)
    return (facesfound,len(facesfound))

def train_faces(Name):
    print('Please stand in a bright place and look towards the camera.')
    cam=cv2.VideoCapture(0)
    _,frame = cam.read()
    frame = cv2.flip(frame,-1)
    image= frame.copy()
    with open('Encodings.pkl','rb') as f:
        known_face_encodings = pickle.load(f)
    with open('Names.pkl','rb') as f:
        known_face_names = pickle.load(f)
    face_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(Name)
    with open('Names.pkl','wb') as f:
        pickle.dump(known_face_names, f)
    with open('Encodings.pkl','wb') as f:
        pickle.dump(known_face_encodings, f)
    print ('Data registered')
