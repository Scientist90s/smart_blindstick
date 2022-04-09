import base64
from clip_local import generate_Inference
from transformers import ViltProcessor
processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
from transformers import ViltForQuestionAnswering 
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
import torch
import os
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import cv2 as cv
import numpy as np
import json
import random

class server():
    def __init__(self):
        # initializing flask
        self.app = Flask(__name__)
        CORS(self.app)
        self.file_name = "./assets/images/received_image.jpg"
        
        # adding routes
        self.app.add_url_rule("/clip", view_func=self.clip_inference, methods=["POST"])
        self.app.add_url_rule("/vilt", view_func=self.vilt_inference, methods=["POST"])
        self.app.add_url_rule("/image", view_func=self.image_inference, methods=["GET"])
        
        # starting flask server
        self.host = "10.0.2.15"
        self.app.run(host=self.host)
        self.random_number = 1

    # Function to call for "/clip" route
    def clip_inference(self):
        if request.method == "POST":
            image_url = self.getImageUrl()
            data = request.get_json(force=True)
            frame = cv.imread(image_url)
            string = base64.b64encode(cv.imencode('.jpg', frame)[1]).decode()
            frame = string
            url = frame
            img_bytes = base64.b64decode(url)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv.imdecode(nparr, cv.IMREAD_COLOR)
            inference = self.clip(img)
            print(inference)
            response = {"inference": f"{inference}"}
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
    
    # Function to call for "/vilt" route
    def vilt_inference(self):
        if request.method == "POST":
            image_url = self.getImageUrl()
            data = request.get_json(force=True)
            frame = cv.imread(image_url)
            string = base64.b64encode(cv.imencode('.jpg', frame)[1]).decode()
            frame = string
            url = frame
            img_bytes = base64.b64decode(url)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv.imdecode(nparr, cv.IMREAD_COLOR)
            que = data["que"]
            ans = self.VQA(img, que)
            print(ans)
            response = {"ans": f"{ans}"}
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
    
    # Function to change the image
    def image_inference(self):
        if request.method == "GET":
            image_choices = [1,2,3,4,5,6,7,8,9,10,11,12]
            self.random_number = random.choice(image_choices)
            random_number_json = jsonify(self.random_number)
            random_number_json.headers.add('Access-Control-Allow-Origin', '*')
        return random_number_json
        
    # Function to do ViLT inference
    def VQA(self, img, ques):
        image = img
        text = ques
        
        encoding = processor(image, text, return_tensors="pt")
        for k,v in encoding.items():
            print(k, v.shape)

        # forward pass
        outputs = model(**encoding)
        logits = outputs.logits
        idx = torch.sigmoid(logits).argmax(-1).item()
        print("Predicted answer:", model.config.id2label[idx])
        
        return model.config.id2label[idx]
    
    # Function to get what image we are looking at
    def getImageUrl(self):
        image_url = '../assets/images/6212487_1cca7f3f_1024x1024.jpg'
        if self.random_number == 1:
            image_url = '../assets/images/COCO_val2014_000000060623.jpg'
        elif self.random_number == 2:
            image_url = '../assets/images/COCO_val2014_000000165547.jpg'
        elif self.random_number == 3:
            image_url = '../assets/images/COCO_val2014_000000354533.jpg'
        elif self.random_number == 4:
            image_url = '../assets/images/COCO_val2014_000000386164.jpg'
        elif self.random_number == 5:
            image_url = '../assets/images/COCO_val2014_000000562207.jpg'
        elif self.random_number == 6:
            image_url = '../assets/images/COCO_val2014_000000579664.jpg'
        elif self.random_number == 7:
            image_url = '../assets/images/CONCEPTUAL_01.jpg'
        elif self.random_number == 8:
            image_url = '../assets/images/CONCEPTUAL_02.jpg'
        elif self.random_number == 9:
            image_url = '../assets/images/CONCEPTUAL_03.jpg'
        elif self.random_number == 10:
            image_url = '../assets/images/CONCEPTUAL_04.jpg'
        elif self.random_number == 11:
            image_url = '../assets/images/CONCEPTUAL_05.jpg'
        else:
            image_url = '../assets/images/CONCEPTUAL_06.jpg'
        return image_url

    # Function to do clip inference
    def clip(self, img):
        weights_path = os.path.join(os.getcwd(),"clip_pretrained_models","conceptual_weights.pt")
        is_gpu = True
        return(generate_Inference(weights_path, img, is_gpu))
    
if __name__ == "__main__":
    server()
