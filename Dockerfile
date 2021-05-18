From python:3.8
RUN apt update && apt install -y tesseract-ocr
RUN apt update && apt install -y libtesseract-dev
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
#command to be executed to run the app
CMD [ "gunicorn","-b",":5000","main:app" ]