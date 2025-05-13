FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libportaudio2 portaudio19-dev

RUN pip install --upgrade pip

COPY docker-requirements.txt .

RUN pip install -r docker-requirements.txt

COPY ./examples/gear/encoder.pickle .
COPY ./examples/gear/model.pickle .

COPY ./examples/speech/models.tflite .
COPY ./examples/speech/tos.scorer .

COPY docker.py .

CMD ["python", "docker.py"]