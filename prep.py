import cv2
import numpy as np

def grayscale(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def thresholding(img):
    blur = cv2.GaussianBlur(img,(5,5),0)
    return cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1] #returns a tuple
       
def erode(img):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(img, kernel, iterations = 1)

def dilate(img):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5)) #for rectangle shape kernel
    return cv2.dilate(img, kernel, iterations=3)
  

def opening(img):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def closing(img):
    kernel = np.ones((10,20),np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)


def canny(image):
    return cv2.Canny(image, 100, 200)

def remove_noise(img):
    img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    gray= grayscale(img)
    blur= cv2.GaussianBlur(gray, (9, 9), 0)
    op= opening(blur)
    img = thresholding(op)
    imgg= canny(img)
    cv2.imshow("fr",imgg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return imgg

def skew_correction_plaintext(image):
    def find_angle(img):
        gray= grayscale(img)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        gray1=cv2.bitwise_not(blur)
        thresh= thresholding(gray1)
    
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5)) #for rectangle shape kernel
        dilate = cv2.dilate(thresh, kernel, iterations=3)

        # Find all contours
        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)

        # Find largest contour and surround in min area box
        largestContour = contours[0]
        minAreaRect = cv2.minAreaRect(largestContour)
        #draw the rectangle on contour
        box = np.int0(cv2.boxPoints(minAreaRect))
        rect=cv2.drawContours(img, [box], 0, (36,255,12), 3)
       

        # Determine the angle. Convert it to the value that was originally used to obtain skewed image
        angle = minAreaRect[-1]
        if angle < -45:
            angle = (90 + angle)
        else:
            angle= angle
        print("[INFO] angle:  {:.3f}".format(angle))
        return  angle
   
    def rotateImage(img, angle: float):
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        newImage = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return newImage
    
    angle= find_angle(image)
    
    imgnew= rotateImage(image, angle)
    
    return imgnew


def skew_correction_textwithbg(image):
    def find_angle(img):
        img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        gray= grayscale(img)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh= thresholding(gray)
    
    
        dilate= closing(thresh) # gives more accurate contour than dilated 
        


        # Find all contours
        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)

        # Find largest contour and surround in min area box
        largestContour = contours[0]
        minAreaRect = cv2.minAreaRect(largestContour)
        
        #draw the rectangle on contour
        box = np.int0(cv2.boxPoints(minAreaRect))
        rect=cv2.drawContours(img, [box], 0, (36,255,12), 3)
        
        # Determine the angle. Convert it to the value that was originally used to obtain skewed image
        angle = minAreaRect[-1]
        if angle < -45:
            angle = (90 + angle)
        else:
            angle= angle
        print("[INFO] angle:  {:.3f}".format(angle))
        return  angle

    def rotateImage(img, angle: float):
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        newImage = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return newImage
    
    angle= find_angle(image)
    imgnew= rotateImage(image, angle)
    return imgnew

def contrast(img):
    #-----Converting image to LAB Color model----------------------------------- 
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)
    
    #-----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    
    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl,a,b))
    
    #-----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    return final
    

#for image type plain text: 1, skewed plain text:2, text with bg :3 , skewed text with bg : 4,   
def processed_img(img,img_type):
    
    if img_type == 1:
        image= contrast(img) 
    elif img_type == 2: 
        image= skew_correction_plaintext(img)
    elif img_type == 3: 
        image= skew_correction_textwithbg(img)
        #print("type of image: ",type(img))
    elif img_type == 4: 
        pass
    elif img_type == 5:
        image=img
    
    return image


if __name__== "__main__":
    img=cv2.imread("/home/nisha/Desktop/sk3.png")
    img=processed_img(img,2)
    cv2.imshow("gfh",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()