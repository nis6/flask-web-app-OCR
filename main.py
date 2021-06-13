from ast import Bytes
from flask import Flask, request, render_template, jsonify
from PIL import Image
import cv2
import os
from io import BytesIO
import numpy as np
from base64 import b64encode
import base64
import sys
# import tesserocr
import east
import pytess
import prep

app = Flask(__name__) #instance creation of Flask class


def output(image,img_type):
    print(img_type)
    if  int(img_type)<= 4:
        img_type=int(img_type)
        img=prep.processed_img(image,img_type)
        text,bounding_box=pytess.image_to_text(img)
    elif int(img_type) ==5:
        text=''
        bounding_box=east.bounding_boxes(image)[0]      
    elif int(img_type)==6:
        configr=r'outputbase digits --oem 3 --psm 6 '
        text,bounding_box=pytess.image_to_text(image,configr)
    elif int(img_type)==7:
        configr=r'outputbase digits --oem 3 --psm 6  -c tessedit_char_whitelist=0123456789'
        text,bounding_box=pytess.image_to_text(image,configr)
    
    bounding_box = cv2.resize(bounding_box,(250,250),interpolation=cv2.INTER_NEAREST)
    return text,bounding_box

@app.route("/")
def home():
    return render_template("home.html")



@app.route("/submit", methods=["POST","GET"])
def form_submit():

    img = request.files["input_image"]
    
    img_as_blob=img.read()
    num=request.form.get("image_type")
    image = Image.open(BytesIO(img_as_blob)).convert("RGB")
    image = np.array(image)
    print("array",type(image))
    # HYPOTHETICAL FN IS CALLED HERE
    # And output is stored
    try:
        recognised_text, bbox_image = output(image,num)
    except:
    
        return render_template("error.html")
    
    # assumption: recognised_text is str, bbox_image is numpy array containing image

    buffer = BytesIO()
    bbox_image = Image.fromarray(bbox_image)
    bbox_image.save(buffer, "jpeg")

    blob = buffer.getvalue()
    base64_blob = b64encode(blob).decode("utf-8")
    #h,w=base64_blob.shape
    
    return render_template("indexocr.html",recognised_text=recognised_text,base64_blob=base64_blob)


@app.route("/submitlive", methods=["POST","GET"])
def form_submit2():

    image = request.form.get("image-live")
    num=request.form.get("image_type")
    print(image)
    decoded_data = base64.b64decode(image)
    #decode_data is bytes-like-object-data, cv2 needs array of numpy bytes
    decoded_data = np.array(list(decoded_data), dtype=np.byte)
    # imdecode reads img from buffer in the memory which here is a byte array
    img = cv2.imdecode(decoded_data, cv2.IMREAD_COLOR)
    
    # HYPOTHETICAL FN IS CALLED HERE
    # And output is stored
    try:
        recognised_text, bbox_image = output(img,num)
    except:
    
        return render_template("error.html")
    
    # assumption: recognised_text is str, bbox_image is numpy array containing image
    #open an IO stream
    buffer = BytesIO()
    #returns an image object ????this image object is bytes, right??
    bbox_image = Image.fromarray(bbox_image)
    #save the img object to memory(buffer) 
    bbox_image.save(buffer, "jpeg")
    #get the bytes out of buffer
    blob = buffer.getvalue()
    #encode the bytes back into base64 and then decode into utf-8
    base64_blob = b64encode(blob).decode("utf-8")
    #h,w=base64_blob.shape
    
    return render_template("indexocr.html",recognised_text=recognised_text,base64_blob=base64_blob)


#if __name__ == "__main__":
    #app.run(host='0.0.0.0',port=5000,debug=True)
