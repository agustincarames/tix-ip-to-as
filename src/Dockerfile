FROM python:3.4.7-slim
MAINTAINER Agustin Carames <aecarames@gmail.com>

RUN apt update
RUN apt install -y python-mysqldb libmysqlclient-dev gcc

RUN pip install --upgrade pip
COPY requirements.txt /root
RUN pip install -r /root/requirements.txt

RUN mkdir /root/iptoas
WORKDIR /root/iptoas
COPY *.py /root/iptoas/

CMD ["python", "main.py"]
