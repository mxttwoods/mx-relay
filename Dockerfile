FROM python:3.9-slim-buster

WORKDIR /app

COPY req.txt req.txt
RUN pip3 install -r req.txt

COPY . .

CMD [ "gunicorn", "-w" , "4", "-b", "127.0.0.1:5000", "app:app"]
