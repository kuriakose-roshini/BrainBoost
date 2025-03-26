import cv2
import os
import numpy as np
from django.conf import settings


class FaceRecognition:
    def __init__(self):
        self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.dataset_path = os.path.join(settings.MEDIA_ROOT, 'face_data')

        if not os.path.exists(self.dataset_path):
            os.makedirs(self.dataset_path)

    def capture_images(self, user_id, num_images=60):
        cam = cv2.VideoCapture(0)
        count = 0
        user_path = os.path.join(self.dataset_path, str(user_id))

        if not os.path.exists(user_path):
            os.makedirs(user_path)

        while count < num_images:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1
                cv2.imwrite(f"{user_path}/{count}.jpg", gray[y:y + h, x:x + w])
                cv2.imshow('Register Face', img)

            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break

        cam.release()
        cv2.destroyAllWindows()
        self.train_model()
        return count

    def train_model(self):
        faces = []
        ids = []

        for user_id in os.listdir(self.dataset_path):
            user_path = os.path.join(self.dataset_path, user_id)

            for image_name in os.listdir(user_path):
                if image_name.endswith('.jpg'):
                    img_path = os.path.join(user_path, image_name)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    faces.append(img)
                    ids.append(int(user_id))

        if len(faces) > 0:
            self.recognizer.train(faces, np.array(ids))
            self.recognizer.save(os.path.join(self.dataset_path, 'trained_model.yml'))

    def load_model(self):
        model_path = os.path.join(self.dataset_path, 'trained_model.yml')
        if os.path.exists(model_path):
            self.recognizer.read(model_path)
            return True
        return False

    def recognize_face(self):
        if not self.load_model():
            return False

        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        recognized = False
        user_id = None

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                id_pred, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])

                if confidence < 60:  # Lower confidence means better match
                    recognized = True
                    user_id = id_pred
                    cv2.putText(img, f"User {id_pred}", (x, y - 5), font, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(img, "Unknown", (x, y - 5), font, 1, (255, 255, 255), 2)

                cv2.imshow('Face Recognition', img)

            k = cv2.waitKey(10) & 0xff
            if k == 27 or recognized:
                break

        cam.release()
        cv2.destroyAllWindows()
        return user_id if recognized else None