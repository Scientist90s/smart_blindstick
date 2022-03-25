import requests
from PIL import Image 
from clip_local import generate_Inference
import os
from flask import Flask, render_template, request, Response
import cv2 as cv
import numpy as np
import json

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./scripts"
img = []
file_name = "received_image.jpg"

@app.route("/image", methods=["POST"])
def home():
    global img
    if request.method == "POST":
        nparr = np.frombuffer(request.data, np.uint8)
        img = cv.imdecode(nparr, cv.IMREAD_COLOR)
        response = {'message': f'image received. size={img.shape[1]}x{img.shape[0]}'}
        response = json.dumps(response)
        return Response(response=response, status=200, mimetype="application/json")


def VQA(url, ques):
    url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    image = Image.open(requests.get(url, stream=True).raw)
    text = "What are cats doing?"

    from transformers import ViltProcessor

    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    encoding = processor(image, text, return_tensors="pt")
    for k,v in encoding.items():
      print(k, v.shape)

    from transformers import ViltForQuestionAnswering 

    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    import torch

    # forward pass
    outputs = model(**encoding)
    logits = outputs.logits
    idx = torch.sigmoid(logits).argmax(-1).item()
    print("Predicted answer:", model.config.id2label[idx])
    return model.config.id2label[idx]

def clip():
    weights_path = os.path.join(os.getcwd(),"assets\clip_pretrained_models\conceptual_weights.pt")
    img_path = os.path.join(os.getcwd(),"assets\images\COCO_val2014_000000386164.jpg")
    is_gpu = True
    generate_Inference(weights_path, img_path, is_gpu)
    
if __name__ == "__main__":
    host = "192.168.0.16"
    app.run(host=host)