##Author:Amartya Kalapahar
##Project: Absolute Face Technologies Internship Assignment

# We will import openCV library for image processing, opening the webcam etc
#Os is required for managing files like directories
#Numpy is basically used for matrix operations
#PIL is Python Image Library
import cv2
import numpy as np
import os 
import json
import pandas as pd
import datetime

#Method for checking existence of path i.e the directory
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def load_names_file():
    try:
        with open(os.path.join(os.path.dirname(__file__),'names.json')) as f:
            return json.load(f)
    except:
        return {}
def add_attendance(name,id):
    file_path = os.path.join(os.path.dirname(__file__),'attendance.xlsx')
    df = pd.DataFrame(columns=['Name', 'ID', 'Date & Time'])
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    items = df.values.tolist()
    items.append([name,id,datetime.datetime.now()])
    df = pd.DataFrame(items,columns=['Name', 'ID', 'Date & Time'])
    df.to_excel(file_path,index=False)


names_obj =load_names_file()
if not names_obj:
    print('Unable to load names.json, please run face_datasets.py first')
    exit(-1)

# Create Local Binary Patterns Histograms for face recognization
recognizer = cv2.face.LBPHFaceRecognizer_create()

assure_path_exists("saved_model/")

# Load the  saved pre trained mode
recognizer.read('saved_model/s_model.yml')

# Load prebuilt classifier for Frontal Face detection
cascadePath = "haarcascade_frontalface_default.xml"

# Create classifier from prebuilt model
faceCascade = cv2.CascadeClassifier(cascadePath);

# font style
font = cv2.FONT_HERSHEY_SIMPLEX

# Initialize and start the video frame capture from webcam
cam = cv2.VideoCapture(0)

# Looping starts here
while True:
    # Read the video frame
    ret, im =cam.read()

    # Convert the captured frame into grayscale
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    # Getting all faces from the video frame
    faces = faceCascade.detectMultiScale(gray, 1.2,5) #default

    # For each face in faces, we will start predicting using pre trained model
    for(x,y,w,h) in faces:


        # Recognize the face belongs to which ID
        Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        #print(Id, confidence)
        if int(confidence) < 40 :
            #create rectangle
            cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
            IdStr = str(Id)
            if IdStr in names_obj:
                name = names_obj[IdStr]
                showStr = "{} {:.2f}%".format(name,round(100 - confidence, 2))
                cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
                cv2.putText(im, str(showStr), (x,y-40), font, 1, (255,255,255), 3)
                print('='*120)
                print('Attendance accepted for: "{}" with ID: "{}"'.format(name,IdStr))
                print('='*120)
                add_attendance(name,IdStr)
                exit(0)
            else:
                showStr = "Unknown {:.2f}%".format(round(100 - confidence, 2))
                cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
                cv2.putText(im, str(showStr), (x,y-40), font, 1, (255,255,255), 3)

        else:
            cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (255,0,0), 4)
            cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (255,0,0), -1)
            cv2.putText(im, "Unknown", (x,y-40), font, 1, (255,255,255), 3)


    # Display the video frame with the bounded rectangle
    cv2.imshow('im',im) 

    # press q to close the program
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Terminate video
cam.release()

# Close all windows
cv2.destroyAllWindows()
