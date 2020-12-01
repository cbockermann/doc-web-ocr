from PIL import Image
import pytesseract
import cv2
import os
import subprocess

def is_executable(fpath):
	return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def _find_convert():
	paths = ["/usr/bin/convert", "/usr/local/bin/convert"]

	for p in paths:
		if is_executable(p):
			return p

	print(f"Cannot find 'convert' in {paths}")
	return None


def image_to_grayscale(image, preprocess=None):
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

def ocr_from_image(image, language='deu'):
	"""
	"""
	print(f"Preprocessing image")
	preprocessed_image = image_to_grayscale(image)

	print("Running OCR (tesseract)...")
	return pytesseract.image_to_string(preprocessed_image, lang=language)


def ocr_from_image_file(file):
	"""
	Diese Funktion liest die übergebene Datei ein und nutzt tesseract um
	OCR auf das Bild in der Datei anzuwenden.

	Die Rückgabe ist der Text, der aus der Datei extrahiert wurde.
	"""
	print(f"ocr_from_image_file:: Reading image from {file}")
	image = cv2.imread(file)
	print(f"image is: {image}")
	return ocr_from_image(image)


def ocr_from_pdf_file(file):
	imageFile = image_from_pdf(file)
	if imageFile is None:
		return None

	print(f" pdf was converted to {imageFile}")
	return ocr_from_image_file(imageFile)

def image_from_pdf(pdfFile):
	"""
	This function call /usr/local/bin/convert to convert the given PDF file into a PNG image.
	The result is the raw image object as returned by the cv2 library from the convert output.
	"""
	convert = _find_convert()
	if convert is None:
		return None

	pngFile = pdfFile.replace(".pdf", ".png")

	cmd = [convert, "-page", "a4", "-colorspace", "RGB", "-alpha", "off", "-density", "200x200", pdfFile + "[0]", pngFile]
	print(f"calling convert: {cmd}")
	subprocess.run(cmd) #, stdout=subprocess.PIPE)
	#data = proc.communicate()[0]
	print(f"Reading data from {pngFile}")
	return pngFile #.imdecode(data, cv2.IMREAD_ANYCOLOR)