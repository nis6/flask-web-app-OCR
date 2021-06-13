from PIL import Image 
from tesserocr import PyTessBaseAPI
import os
import cv2

def image_to_text(image,configr=r'--oem 3 --psm 6 outputbase digits'):
    img = cv2.imread(image)
    cv2.startWindowThread()
    cv2.namedWindow("original")
    cv2.imshow("original",img)
    cv2.waitKey(0)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    #blackwhite = gray.point(lambda x: 0 if x < 200 else 255, '1')
    blackwhite=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    cv2.imwrite(os.path.join("/home/nisha/Downloads","processed_with_pil.jpg"),blackwhite)
    with PyTessBaseAPI() as api:
        api.SetImageFile(os.path.join("/home/nisha/Downloads","processed_with_pil.jpg"))
        text= api.GetUTF8Text()
        conf=api.AllWordConfidences()
    return text, conf

if __name__ =="__main__":
    image='/home/nisha/Desktop/dw.jpeg'
    
    text,conf = image_to_text(image)
    print("text",text)
    print("confidence",conf)


