from pytesseract import Output
import pytesseract as tess
import cv2
from pytesseract.pytesseract import image_to_data
import prep

def image_to_text(image,configr=''):
    tess.pytesseract.tesseract_cmd=r'/usr/bin/tesseract'
    img=prep.grayscale(image)
    if configr=='':
        print("this is config: ")
        text= tess.image_to_string(img)
    else:
        text=tess.image_to_string(img,config=configr)
    print("text from the img:\n",text)
    d = tess.image_to_data(img, output_type=Output.DICT)
    # print("d is type of %s\t", type(d))
    # print(d.keys())
    # print(d["text"])
    
    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            imgb = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
   
    return (text,imgb) 

if __name__== "__main__":
    img=cv2.imread("/home/nisha/Desktop/original.jpg")
    img_type=3
    cv2.startWindowThread()
    cv2.namedWindow("original")
    cv2.imshow("original",img)
    cv2.waitKey(0)
    img=prep.processed_img(img,img_type)
    cv2.startWindowThread()
    cv2.namedWindow("original")
    cv2.imshow("original",img)
    cv2.waitKey(0)
    text, bb=image_to_text(img)

    d=tess.image_to_data(img)
   
    # num_of_words = len(d['text'])
    # for i in range(num_of_words):
    #     print(d['conf'][i])
    cv2.startWindowThread()
    cv2.namedWindow("gfh")
    cv2.imshow("gfh",bb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    