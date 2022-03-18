import cv2
#from pygsr import Pygsr


def text2audio(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def askQuestion():
    
    speech = Pygsr()
    # duration in seconds
    speech.record(3)
    # select the language
    phrase, complete_response = speech.speech_to_text('en_US')

    print(phrase)

def main():
    cam = cv2.VideoCapture(0)
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