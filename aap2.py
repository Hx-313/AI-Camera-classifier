import tkinter as tk
from tkinter import * 
from tkinter import simpledialog
from tkinter import messagebox
import cv2 as cv
import os
import PIL.Image, PIL.ImageTk
from PIL import Image , ImageTk
import model2
import camera2
window=tk.Tk()
image_0 = Image.open("image2.jpeg") 
class App:

    def __init__(self, window_title="Camera Classifier"):
        window.title("Hx's Camera Classifier")
        window.geometry("800x500")
    
        bg_image = ImageTk.PhotoImage(image_0)
        lbl=Label(window , image =bg_image )
        lbl.place(x=0,y=0, relwidth =1 , relheight=1)
        self.window = window
        self.window_title = window_title
        

        self.counters = [1, 1, 1]
        self.model2 = model2.Model()

        self.auto_predict = False

        self.camera = camera2.Camera()

        self.init_gui()

        self.delay = 15
        self.update()

        self.window.attributes('-topmost', True)
        self.window.mainloop()
 
    def init_gui(self):

        self.canvas = tk.Canvas(self.window, bd=1, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()
        response = 0
        if os.path.getsize('Data.txt') == 0:
            tk.messagebox.showerror(" Empty "," No previous data found")
        else:
            response = messagebox.askyesno(" Previous Data Found!", " Do you want to use previous data to train model" )
        if response == 0: 
                self.classname_one = simpledialog.askstring("Classname One", "Enter the name of the first class:", parent=self.window)
                self.classname_two = simpledialog.askstring("Classname Two", "Enter the name of the second class:", parent=self.window)
                self.classname_three = simpledialog.askstring("Classname Three", "Enter the name of the Third class:", parent=self.window)
                with  open('Data.txt', 'w') as file:

                    self.classname_one1 =self.classname_one + ' '
                    self.classname_two1 = self.classname_two +' '
                    self.classname_three1= self.classname_three + ' ' 
                    file.write(self.classname_one1)
                    file.write(self.classname_two1)
                    file.write(self.classname_three1)

        if response == 1:
        
            with  open('Data.txt') as file:
                list = [ word for line in file for word in line.split()]

                self.classname_one = list[0]
                self.classname_two = list[1]
                self.classname_three= list[2]                           
        self.btn_toggleauto = tk.Button(self.window, bg="lemon chiffon", text="Auto Prediction", width=50, command=self.auto_predict_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_one = tk.Button(self.window,bg="dark orchid" , text=self.classname_one, width=50, command=lambda: self.save_for_class(1))    
        self.btn_class_one.pack(anchor=tk.CENTER, expand=True)
        self.btn_class_two = tk.Button(self.window, bg="dark orchid", text=self.classname_two, width=50, command=lambda: self.save_for_class(2))
        self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

        self.btn_class_three = tk.Button(self.window, bg="dark orchid", text=self.classname_three, width=50, command=lambda: self.save_for_class(3))
        self.btn_class_three.pack(anchor=tk.CENTER, expand=True)
    
        self.btn_train = tk.Button(self.window,bg="cyan",  text="Train Model", width=50, command=lambda: self.model2.train_model(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_predict = tk.Button(self.window,bg="green", text="Predcit", width=50, command=self.predict)
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        self.btn_reset = tk.Button(self.window,bg="red", text="Reset", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)

        self.class_label = tk.Label(self.window, text="CLASS")
        self.class_label.config(font=("Chiller", 20))
        self.class_label.pack(anchor=tk.CENTER, expand=True)


    def auto_predict_toggle(self):
        self.auto_predict = not self.auto_predict

    def save_for_class(self, class_num):
        ret, frame = self.camera.get_frame()
        if not os.path.exists('1'):
            os.mkdir('1')

        if not os.path.exists('2'):
            os.mkdir('2')
        if not os.path.exists('3'):
            os.mkdir('3')
        cv.imwrite(f'{class_num}/frame{self.counters[class_num-1]}.jpg' , cv.cvtColor(frame, cv.COLOR_RGB2BGR))
        img = PIL.Image.open(f'{class_num}/frame{self.counters[class_num - 1]}.jpg')
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save(f'{class_num}/frame{self.counters[class_num - 1]}.jpg')

        self.counters[class_num - 1] += 1

    def reset(self):
        for directory in ['1', '2', '3']:
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path) #deleting

        self.counters = [1, 1, 1]
        self.model2 = model2.Model()
        self.class_label.config(text="CLASS")

    def update(self):
        if self.auto_predict:
            self.predict()

        ret, frame = self.camera.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def predict(self):
        frame = self.camera.get_frame()
        prediction = self.model2.predict(frame)

        if prediction == 1:
            self.class_label.config(text=self.classname_one)
            return self.classname_one
        if prediction == 2:
            self.class_label.config(text=self.classname_two)
            return self.classname_two
        if prediction == 3:
            self.class_label.config(text=self.classname_three)
            return self.classname_three

