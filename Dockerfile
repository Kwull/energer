FROM python:3.8.2-slim
LABEL maintainer="Uladzimir Kazakevich"

RUN add-apt-repository ppa:alex-p/tesseract-ocr-devel

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y \
    tesseract-ocr \
	tesseract-ocr-eng \
    libopencv-dev \
    python-pip

RUN pip install --no-cache-dir opencv-python numpy pytesseract paho-mqtt pyyaml

COPY /config/* /config/
COPY energer.py .

VOLUME /config

CMD [ "python", "./energer.py" ]

