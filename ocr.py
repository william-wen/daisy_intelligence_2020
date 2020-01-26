# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import os

def convert_img_to_text(image_path):
	text = pytesseract.image_to_string(Image.open(image_path))
	text = text.lower()

	if len(text.split()) > 5:
		with open("text_output.txt", "a") as f:
			f.write("\n")
			f.write("#######################{}########################".format(image_path))
			f.write("\n")
			f.write(text)
			f.write("\n")
