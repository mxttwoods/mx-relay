import configparser
import logging.config
import smtplib
import ssl
import os
import sys
import yaml
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mail.db"
db = SQLAlchemy(app)

config = configparser.ConfigParser()
config.read("conf.ini")

USERNAME = config.get("settings", "user")
PASSWORD = config.get("settings", "pass")
PORT = config.getint("settings", "port")
SMTP = config.get("settings", "smtp_server")
CONTEXT = ssl.create_default_context()

with open("log.yaml", "r") as conf:
    logger_config = yaml.safe_load(conf.read())
    logging.config.dictConfig(logger_config)

logger = logging.getLogger("main")

logger.info("PORT: %s", PORT)
logger.info("USERNAME: %s", USERNAME)
logger.info("PASSWORD: %s", PASSWORD)
logger.info("SMTP: %s", SMTP)


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=False, nullable=False)
    message = db.Column(db.String(200), unique=False, nullable=False)
    success = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return "<Email(email='%s', message='%s', success='%s')>" % (
            self.email,
            self.message,
            self.success,
        )


db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    return "Hello World!", 200


@app.route("/api/v2/mail", methods=["POST"])
def send_mail_v2():
    if request.method == "POST":
        email = request.args.get("email", default=None, type=str)
        message = request.args.get("message", default=None, type=str)
        global USERNAME
        global PASSWORD
        global PORT
        global SMTP
        global CONTEXT

        try:
            with smtplib.SMTP_SSL(SMTP, PORT, context=CONTEXT) as server:
                server.login(USERNAME, PASSWORD)
                server.sendmail(USERNAME, email, message)
        except Exception as e:
            response = jsonify({"status": "error", "exception": e})
            logger.error(response)
            return response, 500

        db.session.add(Email(email=email, message=message, success=True))
        db.session.commit()

        response = jsonify({"message": message, "email": email, "status": "success"})
        logging.info(response)
        return response, 200


@app.route("/api/v1/mail/<email>/<message>", methods=["POST"])
def send_mail(email, message):
    if request.method == "POST":
        global USERNAME
        global PASSWORD
        global PORT
        global SMTP
        global CONTEXT

        try:
            with smtplib.SMTP_SSL(SMTP, PORT, context=CONTEXT) as server:
                server.login(USERNAME, PASSWORD)
                server.sendmail(USERNAME, email, message)
        except Exception as e:
            response = jsonify({"status": "error", "exception": e})
            logger.error(response)
            return response, 500

        db.session.add(Email(email=email, message=message, success=True))
        db.session.commit()

        response = jsonify({"message": message, "email": email, "status": "success"})
        logger.info(response)
        return response, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
