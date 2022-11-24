FROM python:3.8
MAINTAINER Andrey Tikhonov "andrey.tikhonov@ukr.net"
RUN apt-get update
ADD app app
RUN bash -c 'pip3 install -r /app/requirements.txt'
WORKDIR /app
ENTRYPOINT ["python", "main.py"]

