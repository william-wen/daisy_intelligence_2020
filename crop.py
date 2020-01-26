import cv2
import argparse
from ocr import convert_img_to_text
import os
from PIL import Image

files = [
    file for file in os.listdir("flyer_images") if ".jpg" in file
]

# Load the image
for file in files:
    print("FILE PROCESSING: {}".format(file))

    img = cv2.imread("flyer_images/{}".format(file))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)

    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)

    thresh = cv2.dilate(thresh,None,iterations = 18)
    thresh = cv2.erode(thresh,None,iterations = 30)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for i, cnt in enumerate(contours):
        x,y,w,h = cv2.boundingRect(cnt)

        if h < 150 or w < 150:
            continue

        x_top_left_corner = x - 150
        y_top_left_corner = y - 30

        x_bottom_right_corner = x + w + 150
        y_bottom_right_corner = y + h + 80

        # cv2.rectangle(
        #     img,
        #     (x_top_left_corner, y_top_left_corner),
        #     (x_bottom_right_corner, y_bottom_right_corner),
        #     (0,255,0),
        #     0
        # )

        crop_img = img[
            y_top_left_corner:y_bottom_right_corner,
            x_top_left_corner:x_bottom_right_corner
        ]

        try:
            temp_file = "cropped_images/{}".format(file)
            cv2.imwrite(temp_file, crop_img)
            convert_img_to_text(temp_file)
            os.remove(temp_file)

        except cv2.error:
            with open("error_images.txt", "a") as f:
                f.write(file)

    # cv2.imwrite('img.jpg',img)
