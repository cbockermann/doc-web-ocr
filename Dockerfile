from ubuntu:20.04

# Setup timezone to Europe/Berlin
#
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get -y install tesseract-ocr tesseract-ocr-deu python3-flask wget gnupg python3-venv python3-opencv imagemagick


# The following lines will install elasticsearch. Not required, for now.
#
#RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
#RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-7.x.list
#RUN apt-get update && apt-get install elasticsearch


# Create docweb folders
#
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
