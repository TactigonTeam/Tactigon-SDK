FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential python3-dev bluez bluetooth build-essential gcc libportaudio2 portaudio19-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY docker-requirements.txt .

RUN pip install -r docker-requirements.txt

COPY ./examples/gesture/encoder.pickle .
COPY ./examples/gesture/model.pickle .

COPY ./examples/speech/models.tflite .
COPY ./examples/speech/tos.scorer .

COPY docker.py .

CMD ["python", "docker.py"]