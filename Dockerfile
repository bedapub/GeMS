FROM python:3.7
LABEL maintainer="swk30@cam.ac.uk"
ADD ./requirements.txt .
RUN pip install -r requirements.txt
ADD ./logging.conf .
COPY . /app
WORKDIR /app/src/api
CMD ["gunicorn", "--bind", "0.0.0.0:1234", "wsgi:app"]
