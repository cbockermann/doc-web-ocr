from ubuntu:20.04

RUN apt-get update
RUN apt-get -y install tesseract-ocr tesseract-ocr-deu
RUN apt-get -y install python3-flask
RUN apt-get -y install wget gnupg2
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-7.x.list
RUN apt-get update && apt-get install elasticsearch
RUN mkdir /docweb/
RUN mkdir /docweb/incoming
COPY test/test-document.png /docweb/incoming

ENTRYPOINT ["/bin/bash"]
