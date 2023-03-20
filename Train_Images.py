import cv2
cv2.ocl.setUseOpenCL(False)
import os
import numpy as np

# Create a face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Load images and labels
faces = []
labels = []
for root, dirs, files in os.walk("TrainingImages"):
    for file in files:
        if file.endswith("jpg"):
            path = os.path.join(root, file)
            label = int(os.path.basename(root).split("_")[0])
            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            if len(face) == 1:
                (x, y, w, h) = face[0]
                face_roi = gray[y:y+h, x:x+w]
                faces.append(face_roi)
                labels.append(label)

# Train the face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(labels))

# Save the trained face recognizer to a file
recognizer.save("face_recognizer.xml")
