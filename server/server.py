import base64
import requests
from PIL import Image 
from clip_local import generate_Inference
from transformers import ViltProcessor
processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
from transformers import ViltForQuestionAnswering 
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
import torch
import os
from flask import Flask, render_template, request, Response
import cv2 as cv
import numpy as np
import json

app = Flask(__name__)
file_name = "./assets/images/received_image.jpg"

@app.route("/clip", methods=["POST"])
def clip_inference():
    if request.method == "POST":
        data = request.get_json(force=True)
        img_bytes = base64.b64decode(data["img"])
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv.imdecode(nparr, cv.IMREAD_COLOR)
        inference = clip(img)
        print(inference)
        response = {'message': 'image received', "inference": f"{inference}"}
        response = json.dumps(response)
        return Response(response=response, status=200, mimetype="application/json")
    
@app.route("/vilt", methods=["POST"])
def vilt_inference():
    if request.method == "POST":
        data = request.get_json(force=True)
        img_bytes = base64.b64decode(data["img"])
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv.imdecode(nparr, cv.IMREAD_COLOR)
        que = data["img"]
        ans = VQA(img, que)
        print(ans)
        response = {'message': 'received', "ans": f"{ans}"}
        response = json.dumps(response)
        return Response(response=response, status=200, mimetype="application/json")


def VQA(img, ques):
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

def clip(img):
    weights_path = os.path.join(os.getcwd(),"assets\clip_pretrained_models\conceptual_weights.pt")
    img_path = os.path.join(os.getcwd(),"assets\images\COCO_val2014_000000386164.jpg")
    is_gpu = True
    return(generate_Inference(weights_path, img_path, is_gpu))
    
if __name__ == "__main__":
    host = "192.168.0.16"
    app.run(host=host)