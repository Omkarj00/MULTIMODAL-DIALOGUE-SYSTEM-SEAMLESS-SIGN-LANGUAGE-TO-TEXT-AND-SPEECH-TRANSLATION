import numpy as np
import cv2  # For video playback and image processing
import os
import sys
import time
import operator
from string import ascii_uppercase
import tkinter as tk
from tkinter import Text, END, messagebox
from tkinter.scrolledtext import ScrolledText  
from pathlib import Path  
import speech_recognition as sr   # type: ignore
from PIL import Image, ImageTk  
from spellchecker import SpellChecker   # type: ignore
from keras.models import model_from_json # type: ignore


os.environ["THEANO_FLAGS"] = "device=cuda, assert_no_cpu_op=True"
animation_dir = r"D:\application\Animations"

# Application:
class Application:
    def __init__(self):
        self.spell = SpellChecker(language='en')  
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.current_image2 = None

        # Load Models
        self.json_file = open("D:/application/Models/model_new.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()
        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights("D:/application/Models/model_new.h5")

        self.json_file_dru = open("D:/application/Models/model-bw_dru.json", "r")
        self.model_json_dru = self.json_file_dru.read()
        self.json_file_dru.close()
        self.loaded_model_dru = model_from_json(self.model_json_dru)
        self.loaded_model_dru.load_weights("D:/application/Models/model-bw_dru.h5")

        self.json_file_tkdi = open("D:/application/Models/model-bw_tkdi.json", "r")
        self.model_json_tkdi = self.json_file_tkdi.read()
        self.json_file_tkdi.close()
        self.loaded_model_tkdi = model_from_json(self.model_json_tkdi)
        self.loaded_model_tkdi.load_weights("D:/application/Models/model-bw_tkdi.h5")

        self.json_file_smn = open("D:/application/Models/model-bw_smn.json", "r")
        self.model_json_smn = self.json_file_smn.read()
        self.json_file_smn.close()
        self.loaded_model_smn = model_from_json(self.model_json_smn)
        self.loaded_model_smn.load_weights("D:/application/Models/model-bw_smn.h5")


        self.ct = {'blank': 0}
        self.blank_flag = 0
        for i in ascii_uppercase:
            self.ct[i] = 0
        print("Loaded model from disk")

        # GUI Setup
        self.root = tk.Tk()
        self.root.title("Sign Language To Text Conversion")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("900x900")

        self.root.configure(bg='#7CF5FF')

        self.panel = tk.Label(self.root, bg='#7CF5FF')  
        self.panel.place(x=100, y=10, width=580, height=580)

        # Panel for processed image
        self.panel2 = tk.Label(self.root, bg='#7CF5FF') 
        self.panel2.place(x=400, y=65, width=275, height=275)

        # Title Label
        self.T = tk.Label(self.root, bg='#7CF5FF', fg='black')  
        self.T.place(x=60, y=5)
        self.T.config(text="                 MULTIMODAL DIALOGUE SYSTEM", font=("Courier", 30, "bold"))

        
        self.panel3 = tk.Label(self.root, bg='#7CF5FF', fg='black')  
        self.panel3.place(x=500, y=540)

        # Character label
        self.T1 = tk.Label(self.root, bg='#7CF5FF', fg='black')  
        self.T1.place(x=10, y=540)
        self.T1.config(text="Character :", font=("Courier", 20, "bold"))

        # Word label
        self.panel4 = tk.Label(self.root, bg='#7CF5FF', fg='black')  
        self.panel4.place(x=220, y=595)

        # Word text label
        self.T2 = tk.Label(self.root, bg='#7CF5FF', fg='black')  
        self.T2.place(x=10, y=595)
        self.T2.config(text="Word :", font=("Courier", 20, "bold"))

        # Sentence label
        self.panel5 = tk.Label(self.root, bg='#7CF5FF', fg='black')  
        self.panel5.place(x=350, y=645)

        # Sentence text label
        self.T3 = tk.Label(self.root, bg='#7CF5FF', fg='black')  
        self.T3.place(x=10, y=645)
        self.T3.config(text="Sentence :", font=("Courier", 20, "bold"))

        # Suggestions label
        self.T4 = tk.Label(self.root, bg='#7CF5FF', fg='black')  
        self.T4.place(x=250, y=690)
        self.T4.config(text="Suggestions :", font=("Courier", 20, "bold"))

        
        self.bt1 = tk.Button(self.root, command=self.action1, height=0, width=0, bg='#4F75FF', fg='black')  # Button background color: #4F75FF, text color: black
        self.bt1.place(x=26, y=745)

        self.bt2 = tk.Button(self.root, command=self.action2, height=0, width=0, bg='#4F75FF', fg='black')  # Button background color: #4F75FF, text color: black
        self.bt2.place(x=325, y=745)

        self.bt3 = tk.Button(self.root, command=self.action3, height=0, width=0, bg='#4F75FF', fg='black')  # Button background color: #4F75FF, text color: black
        self.bt3.place(x=625, y=745)

        
        self.str = ""
        self.word = ""
        self.current_symbol = "Empty"
        self.photo = "Empty"

        # Text-to-Sign Language 
        tk.Label(self.root, text="Enter Sentence:", font=("Courier", 20, "bold"), bg="#7CF5FF", fg="black").place(x=1000, y=150)  # Match font and text color
        self.entry = tk.Entry(self.root, width=50)
        self.entry.place(x=1100, y=230)

        self.voice_button = tk.Button(self.root, text="Voice Input", command=self.get_voice_input, bg='#4F75FF', fg='black')  # Button with updated color
        self.voice_button.place(x=1180, y=280)

        self.process_button = tk.Button(self.root, text="Process", command=self.process_text, bg='#4F75FF', fg='black')  # Button with updated color
        self.process_button.place(x=1280, y=280)

        # Processed text
        self.output_label = tk.Label(self.root, text="Processed Text:", font=("Courier", 20, "bold"), bg="#7CF5FF", fg="black")  # Match font and text color
        self.output_label.place(x=1000, y=330)

        self.output_text = Text(self.root, width=38, height=2)
        self.output_text.place(x=1100, y=400)


        self.video_loop()
    def video_loop(self):
        ok, frame = self.vs.read()
        if ok:
            cv2image = cv2.flip(frame, 1)
            x1 = int(0.5 * frame.shape[1])
            y1 = 10
            x2 = frame.shape[1] - 10
            y2 = int(0.5 * frame.shape[1])

            cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), (255, 0, 0), 1)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)

            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            gray = cv2.cvtColor(cv2image[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 2)
            _, res = cv2.threshold(cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                         cv2.THRESH_BINARY_INV, 11, 2), 70, 255, cv2.THRESH_BINARY_INV)

            self.predict(res)

            self.current_image2 = Image.fromarray(res)
            imgtk = ImageTk.PhotoImage(image=self.current_image2)
            self.panel2.imgtk = imgtk
            self.panel2.config(image=imgtk)

            self.panel3.config(text=self.current_symbol, font=("Courier", 30))
            self.panel4.config(text=self.word, font=("Courier", 30))
            self.panel5.config(text=self.str, font=("Courier", 30))

            predicts = list(self.spell.candidates(self.word))

            if len(predicts) > 0:
                self.bt1.config(text=predicts[0], font=("Courier", 20))
            if len(predicts) > 1:
                self.bt2.config(text=predicts[1], font=("Courier", 20))
            if len(predicts) > 2:
                self.bt3.config(text=predicts[2], font=("Courier", 20))

        self.root.after(5, self.video_loop) 
        
    def predict(self, test_image):

        test_image = cv2.resize(test_image, (128, 128))

        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))

        result_dru = self.loaded_model_dru.predict(test_image.reshape(1 , 128 , 128 , 1))

        result_tkdi = self.loaded_model_tkdi.predict(test_image.reshape(1 , 128 , 128 , 1))

        result_smn = self.loaded_model_smn.predict(test_image.reshape(1 , 128 , 128 , 1))

        prediction = {}

        prediction['blank'] = result[0][0]

        inde = 1

        for i in ascii_uppercase:

            prediction[i] = result[0][inde]

            inde += 1

        #LAYER 1

        prediction = sorted(prediction.items(), key = operator.itemgetter(1), reverse = True)

        self.current_symbol = prediction[0][0]


        #LAYER 2

        if(self.current_symbol == 'D' or self.current_symbol == 'R' or self.current_symbol == 'U'):

        	prediction = {}

        	prediction['D'] = result_dru[0][0]
        	prediction['R'] = result_dru[0][1]
        	prediction['U'] = result_dru[0][2]

        	prediction = sorted(prediction.items(), key = operator.itemgetter(1), reverse = True)
        	self.current_symbol = prediction[0][0]

        if(self.current_symbol == 'D' or self.current_symbol == 'I' or self.current_symbol == 'K' or self.current_symbol == 'T'):

        	prediction = {}

        	prediction['D'] = result_tkdi[0][0]
        	prediction['I'] = result_tkdi[0][1]
        	prediction['K'] = result_tkdi[0][2]
        	prediction['T'] = result_tkdi[0][3]

        	prediction = sorted(prediction.items(), key = operator.itemgetter(1), reverse = True)
        	self.current_symbol = prediction[0][0]

        if self.current_symbol == 'M' or self.current_symbol == 'N' or self.current_symbol == 'S':

            prediction = {}

            prediction['M'] = result_smn[0][0]
            prediction['N'] = result_smn[0][1]
            prediction['S'] = result_smn[0][2]

            prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
            self.current_symbol = prediction[0][0]
        
        if(self.current_symbol == 'blank'):

            for i in ascii_uppercase:
                self.ct[i] = 0

        self.ct[self.current_symbol] += 1

        if(self.ct[self.current_symbol] > 60):

            for i in ascii_uppercase:
                if i == self.current_symbol:
                    continue

                tmp = self.ct[self.current_symbol] - self.ct[i]

                if tmp < 0:
                    tmp *= -1

                if tmp <= 20:
                    self.ct['blank'] = 0

                    for i in ascii_uppercase:
                        self.ct[i] = 0
                    return

            self.ct['blank'] = 0

            for i in ascii_uppercase:
                self.ct[i] = 0

            if self.current_symbol == 'blank':

                if self.blank_flag == 0:
                    self.blank_flag = 1

                    if len(self.str) > 0:
                        self.str += " "

                    self.str += self.word

                    self.word = ""

            else:

                if(len(self.str) > 16):
                    self.str = ""

                self.blank_flag = 0

                self.word += self.current_symbol
    def action1(self):
        predicts = list(self.spell.candidates(self.word))
        if len(predicts) > 0:
            self.word = ""
            self.str += " " + predicts[0]

    def action2(self):
        predicts = list(self.spell.candidates(self.word))
        if len(predicts) > 1:
            self.word = ""
            self.str += " " + predicts[1]

    def action3(self):
        predicts = list(self.spell.candidates(self.word))
        if len(predicts) > 2:
            self.word = ""
            self.str += " " + predicts[2]

    def get_voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Voice Input", "Please speak your sentence.")
            try:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                self.entry.delete(0, END)
                self.entry.insert(0, text)
            except sr.UnknownValueError:
                messagebox.showerror("Error", "Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                messagebox.showerror("Error", f"Could not request results; {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {e}")


    def process_text(self):
        # Process input text and convert it to sign language
        text = self.entry.get().strip().lower()
        self.output_text.delete(1.0, END)
        self.output_text.insert(END, f"Processed Text: {text}\n")
        if text:
            words = text.split()
            self.display_animations(words)

    def display_animations(self, words):
        animations = []
        for word in words:
            path = Path(animation_dir) / f"{word}.mp4"
            if path.is_file():
                animations.append(path)
            else:
                for char in word:
                    char_path = Path(animation_dir) / f"{char}.mp4"
                    if char_path.is_file():
                        animations.append(char_path)
        if animations:
            self.play_all_animations(animations)
        else:
            messagebox.showinfo("No Animation", "No animations found for the given sentence or characters.")

    def play_all_animations(self, animations):
        cv2.namedWindow("Animation Playback", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Animation Playback", 400, 300)
        for path in animations:
            cap = cv2.VideoCapture(str(path))
            if not cap.isOpened():
                print(f"Error opening video: {path}")
                continue
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow("Animation Playback", frame)
                if cv2.waitKey(20) & 0xFF == ord("q"):
                    break
            cap.release()
        cv2.destroyWindow("Animation Playback")

    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()

print("Starting Application...")
(Application()).root.mainloop()
