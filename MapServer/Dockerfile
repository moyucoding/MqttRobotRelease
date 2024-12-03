FROM python:3.9-slim-bullseye

WORKDIR /app
ADD . /app

RUN pip3 install --progress-bar off -r ./requirements.txt

EXPOSE 1884

ENTRYPOINT ["python3", "Scripts/mqtthandler.py"]