FROM python:3.9-slim-buster

WORKDIR /app

COPY req.txt req.txt
COPY app.py app.py
COPY log.yaml log.yaml
COPY conf.ini conf.ini

RUN pip3 install -r req.txt

CMD ["gunicorn", "-w" , "4", "-b", "0.0.0.0:5000", "app:app"]
