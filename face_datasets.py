##Author:Amartya Kalapahar
##Project: Absolute Face Technologies Internship Assignment

# We will import openCV library for image processing, opening the webcam etc
#Os is required for managing files like directories
import cv2
import os
import argparse
import json
import datetime

#Method for checking existence of path i.e the directory

def get_person_id():
    return int(datetime.datetime.now().timestamp())


def load_names_file():
    try:
        with open(os.path.join(os.path.dirname(__file__),'names.json')) as f:
            return json.load(f)
    except:
        return {}

def save_names_file(obj):
    try:
        with open(os.path.join(os.path.dirname(__file__),'names.json'),'w') as f:
            json.dump(obj, f)
    except Exception as e:
        print(e)
        print('Error saving names file')

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


parser = argparse.ArgumentParser(description='Face datasets')
parser.add_argument('-n','--name',type=str, help='Name of the person',required=True)

args = parser.parse_args()
names_obj = load_names_file()
face_id = get_person_id()
names_obj[face_id] = args.name

print('Face ID for {} is {}'.format(args.name,face_id))

# save the names dictionary in file
save_names_file(names_obj)

# Starting the web cam by invoking the VideoCapture method
vid_cam = cv2.VideoCapture(0)

# For detecting the faces in each frame we will use Haarcascade Frontal Face default classifier of OpenCV
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# Variable for counting the no. of images
count = 0

#checking existence of path
assure_path_exists("training_data/")

# Looping starts here
while(True):

    # Capturing each video frame from the webcam
    _, image_frame = vid_cam.read()

    # Converting each frame to grayscale image
    gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    # Detecting different faces
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    # Looping through all the detected faces in the frame
    for (x,y,w,h) in faces:

        # Crop the image frame into rectangle
        cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)
        
        # Increasing the no. of images by 1 since frame we captured
        count += 1

        # Saving the captured image into the training_data folder
        cv2.imwrite("training_data/Person." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        # Displaying the frame with rectangular bounded box
        cv2.imshow('frame', image_frame)

    # press 'q' for at least 100ms to stop this capturing process
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

    #We are taking 100 images for each person for the training data
    # If image taken reach 100, stop taking video
    elif count>100:
        break

# Terminate video
vid_cam.release()

# Terminate all started windows
cv2.destroyAllWindows()


