import cv2
import numpy as np
import pytesseract
# import the necessary packages
from imutils.object_detection import non_max_suppression
import pprint
# import tesserocr


min_confidence =60

def reconst(img):
    global h,w
    h=img.shape[0]
    w=img.shape[1]
    hr=int(h/30)*32
    wr=int(w/30)*32
    image=cv2.resize(img,(hr,wr), interpolation=cv2.INTER_NEAREST)
    global rh
    rh=h/hr
    global rw
    rw=w/wr
    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (wr, hr),(123.68, 116.78, 103.94), swapRB=True, crop=False)

    return blob

def decode_predictions(meanscore,scores, geometry):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows): #numRows is no. of text locations
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        

        # loop over the number of columns
        for x in range(0, numCols):  # numCols is number of possible bounding  boxes at a text loc
            # if our score does not have sufficient probability,
            # ignore it

            if scoresData[x] < meanscore:
                continue

            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0) #rownum into y instead of x and vice versa bcz blob interchanges the dim (1,channels,cols,rows)

            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates
            # for the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score
            # to our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)


def bounding_boxes(img):
    blob=reconst(img)
    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet("frozen_east_text_detection.pb")

    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    meanscore=np.mean(scores)

    # decode the predictions, then  apply non-maxima suppression to
    # suppress weak, overlapping bounding boxes
    (rects, confidences) = decode_predictions(meanscore,scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    
    # initialize the list of results
    results = []

    # loop over the bounding boxes
    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rw)
        startY = int(startY * rh)
        endX = int(endX * rw)
        endY = int(endY * rh)

        # # in order to obtain a better OCR of the text we can potentially
        # # apply a bit of padding surrounding the bounding box -- here we
        # # are computing the deltas in both the x and y directions
        # dX = int((endX - startX) * 0.1)
        # dY = int((endY - startY) * 0.1)
        #  # apply padding to each side of the bounding box, respectively
        # startX = max(0, startX - dX)
        # startY = max(0, startY - dY)
        # endX = min(w, endX + (dX * 2))
        # endY = min(h, endY + (dY * 2))


        
        
        # extract the actual padded ROI
        roi = img[startY:endY, startX:endX]
        text = pytesseract.image_to_string(roi)
        results.append(((startX, startY, endX, endY), text))

        imgb=cv2.rectangle(img, (startX, startY), (endX, endY),(0, 0, 255), 2)
        # add the bounding box coordinates and OCR'd text to the list
        # of results
        # results.append(((startX, startY, endX, endY), text))
        # # sort the results bounding box coordinates from top to bottom
    return imgb,results

    
if __name__== "__main__":
    img=cv2.imread("/home/nisha/Desktop/output.jpg")
    # imgm=img.copy()
    # image=reconst(img)
    print(img.shape)
    
   
    imgb,results=bounding_boxes(img)
    # sort the results bounding box coordinates from top to bottom
    results = sorted(results, key=lambda r: r[0][1])
    for ((startX, startY, endX, endY), text) in results:
        # display the text OCR'd by Tesseract
        # print("OCR TEXT")
        # print("========")
        # print("{}\n".format(text))

        # strip out non-ASCII text so we can draw the text on the image
        # using OpenCV, then draw the text and a bounding box surrounding
        # the text region of the input image
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()

    print("here is the text extracted: ",text)
    cv2.startWindowThread()
    cv2.namedWindow("original")
    cv2.imshow("original",imgb)
    cv2.waitKey(0)

    # draw the bounding box on the image
    




    # cv2.startWindowThread()
    # cv2.namedWindow("original")
    # cv2.imshow("original",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imshow("img",image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
