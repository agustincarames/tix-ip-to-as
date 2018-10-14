FROM python:3.4.7-slim

RUN apt update && apt install -y \
	gcc \
	libmysqlclient-dev \
	python-mysqldb

WORKDIR /root
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /root/iptoas
COPY *.py ./
CMD ["python", "main.py"]
