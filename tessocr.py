from PIL import Image 
from tesserocr import PyTessBaseAPI
import os


def image_to_text(image,configr=r'--oem 3 --psm 6 outputbase digits'):
    img = Image.open(image)
    img.show()
    gray = img.convert('L')
    blackwhite = gray.point(lambda x: 0 if x < 200 else 255, '1')
    blackwhite.save(os.path.join("/home/nisha/Downloads","processed_with_pil.jpg"))
    with PyTessBaseAPI() as api:
        api.SetImageFile(os.path.join("/home/nisha/Downloads","processed_with_pil.jpg"))
        text= api.GetUTF8Text()
        conf=api.AllWordConfidences()
    return text, conf

if __name__ =="__main__":
    image='/home/nisha/Downloads/image2.jpg'
    text,conf = image_to_text(image)
    print("text",text)
    print("confidence",conf)