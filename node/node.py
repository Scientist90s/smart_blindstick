import requests
import json
import cv2 as cv
import speech_recognition as sr
import pyttsx3
import base64

img_path = "./assets/images/COCO_val2014_000000386164.jpg"
read_image = True

#  parameters for web api
clip_url = "http://192.168.0.16:5000/clip"
vilt_url = "http://192.168.0.16:5000/vilt"
# content_type = "appl"
# headers = {"content_type" : content_type}

def text2speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def askQuestion():
    print("Inside askQuestion")
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("start speaking")
        audio = r.listen(mic)
        try:
        # using google speech recognition
            inference = r.recognize_google(audio)
            print("Text: "+ inference)
            return(inference)
        except:
            print("Sorry, I did not get that")

def main():
    cam = cv.VideoCapture(0)
    while(True):
        print("Please select 1 if you want to click the picture")
        text2speech("Please select 1 if you want to click the picture")
        option = input()
        if(str(option) == "1"):
            if read_image == True:
                frame = cv.imread(img_path)
            else:
                ret, frame = cam.read()
            _, img_encoded = cv.imencode('.jpg', frame)
            img_base64 = base64.b64encode(img_encoded).decode()
            send_json = {"img": img_base64}
            response = requests.post(clip_url, json=send_json)
            response = response.json()
            print(response)

            #text2audio(inference)
            while(True):
                print("Please select 1 if you want to use VQA for the picture")
                text2speech("Select 1 for VQA")
                boolVQA = input()
                if(str(boolVQA) == "1"):
                    ques = askQuestion()
                    send_json = {"img": img_base64, "que": f"{ques}?"}
                    response = requests.post(vilt_url, json=send_json)
                    response = response.json()
                    print(response)
                    #text2audio(inferenceVQA)

                else:
                    break  
        else:
            pass
        
if __name__ == "__main__":
    main()