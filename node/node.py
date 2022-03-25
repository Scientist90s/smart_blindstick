import requests
import json
import cv2 as cv
import speech_recognition as sr
import pyttsx3
#from pygsr import Pygsr

url = "http://192.168.0.16:5000/image"
content_type = "image/jpeg"
headers = {"content_type" : content_type}

img = cv.imread("./assets/images/COCO_val2014_000000386164.jpg")
_, img_encoded = cv.imencode('.jpg', img)
response = requests.post(url, data=img_encoded.tobytes(), headers=headers)
print(json.loads(response.text))

def text2speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def askQuestion():
    print("Inside askQuestion")
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = r.listen(mic)
        try:
        # using google speech recognition
            print("Text: "+r.recognize_google(audio_text))
        except:
            print("Sorry, I did not get that")

def main():
    cam = cv.VideoCapture(0)
    while(True):
        #text2audio("Please select one if you want to click the picture")
        option = input()
        if(str(option) == "1"):
            ret, frame = cam.read()
            '''
            send frame to server CLIP, async and wait
            inference = received
            
            '''
            #text2audio(inference)
            while(True):
                boolVQA = input()
                if(str(boolVQA) == "1"):
                    #ques = askQuestion()
                    
                    '''
                    send frame along with the question to server ViLT, async and wait
                    inferenceVQA = receivedVQA

                    ''' 
                    #text2audio(inferenceVQA)

                else:
                    break
                
        else:
            pass
        
if __name__ == "__main__":
    askQuestion()