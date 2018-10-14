FROM python:3-slim

# Install app dependencies
RUN apt-get update && apt-get install -y \
	gcc \
	libmariadbclient-dev \
	python-mysqldb

WORKDIR /root
COPY requirements.txt .
RUN pip install -r requirements.txt \
	&& rm -rf /root/.cache

# Bundle app source
WORKDIR /root/iptoas
COPY *.py ./
CMD ["python", "main.py"]
