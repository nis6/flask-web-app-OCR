from flask import Flask, request, render_template, jsonify
from PIL import Image
import cv2
import os
import numpy as np
from io import BytesIO
from base64 import b64encode
import sys
# import tesserocr

import pytess
import prep

app = Flask(__name__)


def output(image,img_type):

    if  int(img_type)<= 5:
        img_type=int(img_type)
        img=prep.processed_img(image,img_type)
        text,bounding_box=pytess.image_to_text(img)
    elif int(img_type)==6:
        configr=r'outputbase digits --oem 3 --psm 6 '
        text,bounding_box=pytess.image_to_text(image,configr)
    elif int(img_type)==7:
        configr=r'outputbase digits --oem 3 --psm 6  -c tessedit_char_whitelist=0123456789'
        text,bounding_box=pytess.image_to_text(image,configr)
          
    return text,bounding_box

@app.route("/")
def home():
    return render_template("home.html")




@app.route("/submit", methods=["POST","GET"])
def form_submit():
    
    img = request.files["input_image"]
    
    img_as_blob = img.read()
    num=request.form["image_type"]


    image = Image.open(BytesIO(img_as_blob)).convert("RGB")
    image = np.array(image)

    # HYPOTHETICAL FN IS CALLED HERE
    # And output is stored
    recognised_text, bbox_image = output(image,num)
    # assumption: recognised_text is str, bbox_image is numpy array containing image

    buffer = BytesIO()
    bbox_image = Image.fromarray(bbox_image)
    bbox_image.save(buffer, "jpeg")
    
    blob = buffer.getvalue()
    base64_blob = b64encode(blob).decode("utf-8")

    return render_template("ocr.html",recognised_text=recognised_text,base64_blob=base64_blob)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
