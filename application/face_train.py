import os
import numpy as np
from PIL import Image
import cv2
import pickle


def train():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(BASE_DIR, 'images')

    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascades/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    y_labels = []
    x_train = []
    current_id = 0
    label_ids = {}

    for root, sirs, files in os.walk(img_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root, file)
                # getting the name of the folder name that is the person name
                label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
                print(path, label)
                # x_train.append(path)
                # y_labels.append(label)
                if not label in label_ids:
                    label_ids[label] = current_id
                    current_id += 1
                id = label_ids[label]
                print(label_ids)
                # take te images and convert them to number arrays
                # convert the images to grey scale and numpy arrays
                pil_image = Image.open(path).convert("L");
                size = (550, 550)
                final_image = pil_image.resize(size, Image.ANTIALIAS)
                image_array = np.array(pil_image, 'uint8')
                print(image_array)
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

                for (x, y, w, h) in faces:
                    interested_region = image_array[y:y + h, x:x + w]
                    x_train.append(interested_region)
                    y_labels.append(id)
    with open("labels.pickle", 'wb') as f:
        # dump the label ids to a file
        pickle.dump(label_ids, f)
    recognizer.train(x_train, np.array(y_labels))
    recognizer.save("trainner.yml")

train()