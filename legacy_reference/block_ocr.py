import cv2
import pytesseract
from ocr import convert_img_to_text
import os

image = cv2.imread("week_1_page_1.jpg")
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
_,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) # threshold
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate
contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours

# for each contour found, draw a rectangle around it on original image
for contour in contours:
    # get rectangle bounding contour
    [x,y,w,h] = cv2.boundingRect(contour)
#     # discard areas that are too large
#     if h>300 and w>300:
#         continue

    # discard areas that are too small
    if h<400 or w<400:
        continue
    
    # draw rectangle around contour on original image
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),10)

    crop_img = image[y:y+h, x:x+w]

    temp_file = "contoured_temp.jpg"
    cv2.imwrite(temp_file, image) 

    convert_img_to_text(temp_file)

    # remove temp file
    os.remove(temp_file)

# write original image with added contours to disk  
# cv2.imwrite("contoured.jpg", image) 
