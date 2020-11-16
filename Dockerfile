from ubuntu:20.04

RUN apt-get update
RUN apt-get -y install tesseract-ocr tesseract-ocr-deu
RUN apt-get -y install python3-flask
COPY test.png /

ENTRYPOINT ["/bin/bash"]
