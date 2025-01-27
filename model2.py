
import tkinter as Tk
from sklearn.svm import LinearSVC
import numpy as np
import cv2 as cv
import PIL

class Model:

    def __init__(self):
        self.model2 = LinearSVC()

    def train_model(self, counters):
        img_list = np.array([])
        class_list = np.array([])

        for i in range(1, counters[0]):
            img = cv.imread(f'1/frame{i}.jpg')[:, :, 0]
            img = img.reshape(16950)
            img_list = np.append(img_list, [img])
            class_list = np.append(class_list, 1)

        for i in range(1, counters[1]):
            img = cv.imread(f'2/frame{i}.jpg')[:, :, 0]
            img = img.reshape(16950)
            img_list = np.append(img_list, [img])
            class_list = np.append(class_list, 2)
        for i in range(1, counters[2]):
            img = cv.imread(f'3/frame{i}.jpg')[:, :, 0]
            img = img.reshape(16950)
            img_list = np.append(img_list, [img])
            class_list = np.append(class_list, 3)

        img_list = img_list.reshape(counters[0] - 1 + counters[1] - 1+ counters[2] - 1, 16950)
        self.model2.fit(img_list, class_list)
        Tk.messagebox.showinfo("Training model", "Model Trained Successfully")

    def predict(self, frame):
        frame = frame[1]
        cv.imwrite("frame.jpg", cv.cvtColor(frame , cv.COLOR_RGB2BGR))
        img = PIL.Image.open("frame.jpg")
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save("frame.jpg")

        img = cv.imread('frame.jpg')[:, :, 0]
        img = img.reshape(16950)
        prediction = self.model2.predict([img])

        return prediction[0]