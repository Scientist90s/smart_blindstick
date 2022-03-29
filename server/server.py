import base64
from clip_local import generate_Inference
from transformers import ViltProcessor
processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
from transformers import ViltForQuestionAnswering 
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
import torch
import os
from flask import Flask, request, Response
import cv2 as cv
import numpy as np
import json

class server():
    def __init__(self):
        # initializing flask
        self.app = Flask(__name__)
        self.file_name = "./assets/images/received_image.jpg"
        
        # adding routes
        self.app.add_url_rule("/clip", view_func=self.clip_inference, methods=["POST"])
        self.app.add_url_rule("/vilt", view_func=self.vilt_inference, methods=["POST"])
        
        # starting flask server
        self.host = "192.168.0.16"
        self.app.run(host=self.host)

    # Function to call for "/clip" route
    def clip_inference(self):
        if request.method == "POST":
            data = request.get_json(force=True)
            img_bytes = base64.b64decode(data["img"])
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv.imdecode(nparr, cv.IMREAD_COLOR)
            cv.imshow("received image",img)
            cv.waitKey()
            inference = self.clip(img)
            print(inference)
            response = {'message': 'image received', "inference": f"{inference}"}
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
    
    # Function to call for "/vilt" route
    def vilt_inference(self):
        if request.method == "POST":
            data = request.get_json(force=True)
            img_bytes = base64.b64decode(data["img"])
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv.imdecode(nparr, cv.IMREAD_COLOR)
            que = data["que"]
            ans = self.VQA(img, que)
            print(ans)
            response = {'message': 'received', "ans": f"{ans}"}
            response = json.dumps(response)
            return Response(response=response, status=200, mimetype="application/json")
        
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

    # Function to do clip inference
    def clip(self, img):
        weights_path = os.path.join(os.getcwd(),"assets\clip_pretrained_models\conceptual_weights.pt")
        is_gpu = True
        return(generate_Inference(weights_path, img, is_gpu))
    
if __name__ == "__main__":
    server()