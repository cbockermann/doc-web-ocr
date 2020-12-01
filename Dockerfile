from ubuntu:20.04

RUN apt-get update
RUN apt-get -y install tesseract-ocr tesseract-ocr-deu
RUN apt-get -y install python3-flask
RUN apt-get -y install wget gnupg2
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-7.x.list
RUN apt-get update && apt-get install elasticsearch
RUN apt-get -y install python3-venv python3-opencv
RUN mkdir /docweb/
RUN mkdir /docweb/incoming
COPY test/test-document.png /docweb/incoming
ADD docweb /docweb
COPY app.py /
RUN python3 -m venv env
RUN . env/bin/activate && pip install opencv-python flask flask_dropzone pillow
RUN . env/bin/activate && pip install pytesseract 
COPY run.sh /run.sh
ADD templates /templates
RUN chmod 777 /run.sh

ENTRYPOINT ["/run.sh"]
