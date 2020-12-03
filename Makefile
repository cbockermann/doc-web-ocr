VERSION=v1

docker:
	docker build -t doc-web-ocr:$(VERSION) .


setup-venv:
	python -m venv env
	. ./env/bin/activate
	pip install --upgrade pip
	pip install flask flask_dropzone Pillow pytesseract opencv-python