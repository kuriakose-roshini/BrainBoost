import cv2
import numpy as np
import os
from PIL import Image

DATASET_PATH = "media/face_images/"
TRAINER_FILE = "media/trainer.yml"
FACE_CASCADE = "haarcascade_frontalface_default.xml"

def train_face_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + FACE_CASCADE)

    image_paths = [os.path.join(DATASET_PATH, f) for f in os.listdir(DATASET_PATH)]
    face_samples = []
    ids = []

    for img_path in image_paths:
        pil_image = Image.open(img_path).convert("L")  # Convert to grayscale
        img_numpy = np.array(pil_image, "uint8")
        user_id = int(os.path.splitext(os.path.basename(img_path))[0].split("_")[-1])  # Extract user ID

        faces = face_cascade.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(user_id)

    if face_samples:
        recognizer.train(face_samples, np.array(ids))
        recognizer.write(TRAINER_FILE)
        print("Face training completed!")
    else:
        print("No faces found for training.")
