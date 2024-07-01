FROM m.daocloud.io/docker.io/library/python:3.9-slim

WORKDIR /app
ADD . /app

RUN pip3 install -r ./requirements.txt

EXPOSE 1884

ENTRYPOINT ["python3", "Scripts/mqtthandler.py"]