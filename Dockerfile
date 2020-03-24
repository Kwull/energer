FROM python:3.8.2
LABEL maintainer="Uladzimir Kazakevich"

RUN echo "deb https://notesalexp.org/tesseract-ocr-dev/buster/ buster main" >> /etc/apt/sources.list 
RUN wget -O - https://notesalexp.org/debian/alexp_key.asc | apt-key add -

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y \
    tesseract-ocr \
	tesseract-ocr-eng \
    libopencv-dev \
    python-pip

RUN pip install --no-cache-dir opencv-python numpy pytesseract paho-mqtt pyyaml

COPY /config/* /config/
COPY /config/lets.traineddata /usr/share/tesseract-ocr/5/tessdata/
COPY energer.py .

VOLUME /config

CMD [ "python", "./energer.py" ]

