FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# https://cloud.google.com/run/docs/tutorials/system-packages#dockerfile
RUN set -ex; \
  apt-get -y update; \
  apt-get -y install imagemagick; \
  rm -rf /var/lib/apt/lists/*

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
