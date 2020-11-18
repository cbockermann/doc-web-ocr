from PIL import Image
import pytesseract
import cv2
import os

def ocr_from_file(file):
	"""
	Diese Funktion liest die übergebene Datei ein und nutzt tesseract um
	OCR auf das Bild in der Datei anzuwenden.

	Die Rückgabe ist der Text, der aus der Datei extrahiert wurde.
	"""
	print(f"Reading image from {file}")
	image = cv2.imread(file)


	print(f"Preprocessing image {file}")
	preprocessed_image = convert_to_grayscale(image)

#	cv2.imshow("Input", image)
#	cv2.imshow("Preprocessed", preprocessed_image)
#	cv2.waitKey(0)

	print("Running OCR (tesseract)...")
	txt = pytesseract.image_to_string(preprocessed_image, lang='deu')

	return txt


def convert_to_grayscale(image, preprocess=None):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# check to see if we should apply thresholding to preprocess the
	# image
	if preprocess == "thresh":
		gray = cv2.threshold(gray, 0, 255,
			cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	# make a check to see if median blurring should be done to remove
	# noise
	elif preprocess == "blur":
		gray = cv2.medianBlur(gray, 3)
	# write the grayscale image to disk as a temporary file so we can
	# apply OCR to it
#	filename = "grayscaled_{}.png".format(os.getpid())
#	cv2.imwrite(filename, gray)
	print("Returning gray-scaled image...")
	return gray
#	print(f"Writing converted image to: {filename}")
#	return filename
