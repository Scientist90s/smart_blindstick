# import libraries
import requests
import cv2 as cv
import speech_recognition as sr
import pyttsx3
import base64

class inference():
    # function to convert text to speech
    def text2speech(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    # function to convert speech to text
    def askQuestion(self):
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            print("start speaking")
            self.text2speech("start speaking")
            audio = r.listen(mic)
            try:
                # using google speech recognition
                inference = r.recognize_google(audio)
                print("Text: "+ inference)
                return(inference)
            except:
                print("Sorry, I did not get that")
                return("Sorry, I did not get that")

    def __init__(self):
        # Important variables for suing image instead of camera
        self.img_path = "./assets/images/COCO_val2014_000000386164.jpg"
        self.read_image = True

        # Web api Links
        self.clip_url = "http://192.168.0.16:5000/clip"
        self.vilt_url = "http://192.168.0.16:5000/vilt"

        # video capturing device handle
        cam = cv.VideoCapture(0)
        
        # Loop for iterating algorithm continuously
        while(True):
            print("Please select 1 if you want to click the picture")
            self.text2speech("Select 1 to click picture")
            option = input()
            if(str(option) == "1"):
                if self.read_image == True:
                    frame = cv.imread(self.img_path)
                else:
                    ret, frame = cam.read()
                    
                # encoding and sending image to server for clip inference
                _, img_encoded = cv.imencode('.jpg', frame)
                img_base64 = base64.b64encode(img_encoded).decode()
                send_json = {"img": img_base64}
                response = requests.post(self.clip_url, json=send_json)
                response = response.json()
                print(response)
                self.text2speech(response["inference"])
                
                # Loop to start VQA session
                while(True):
                    print("Please select 1 if you want to use VQA for the picture")
                    self.text2speech("Select 1 for VQA")
                    boolVQA = input()
                    if(str(boolVQA) == "1"):
                        ques = self.askQuestion()
                        
                        # sending question along with image to server for vilt inference
                        send_json = {"img": img_base64, "que": f"{ques}?"}
                        response = requests.post(self.vilt_url, json=send_json)
                        response = response.json()
                        print(response)
                        self.text2speech(response["ans"])
                    else:
                        break  
            else:
                pass
        
if __name__ == "__main__":
    inference()