import cv2
import cv2.face
import os
import numpy as np
from openpyxl import Workbook

# Path to the folder containing the testing images
folder_path = 'TestingImages/'

# Load the trained face recognizer from the XML file
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.load("face_recognizer.xml")

# Create a list to hold the names of the recognized people
names = []

# Create a dictionary to hold the attendance of each person
attendance = {}

# Create a face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Loop over the images in the testing folder
for image_name in os.listdir(folder_path):
    # Load the image
    image_path = folder_path + image_name
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    # Process each detected face
    for (x, y, w, h) in faces_rect:
        # Extract the face region of interest
        face_roi = gray[y:y+h, x:x+w]
        
        # Use the trained recognizer to predict the label of the person
        label, confidence = recognizer.predict(face_roi)
        
        # Append the name of the recognized person to the list
        names.append(str(label))
        
        # Update the attendance dictionary
        if str(label) not in attendance:
            attendance[str(label)] = 1
        else:
            attendance[str(label)] += 1

# Write the attendance data to an Excel file
workbook = Workbook()
worksheet = workbook.create_sheet(title="Attendance")
header = ["Name", "Attendance"]
worksheet.append(header)
for name, count in attendance.items():
    row = [name, count]
    worksheet.append(row)
workbook.save("attendance/attendance.xlsx")
