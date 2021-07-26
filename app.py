import configparser
import logging.config
import smtplib
import ssl

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
logger.info("Config loaded")

logger.debug("PORT: %s", PORT)
logger.debug("USERNAME: %s", USERNAME)
logger.debug("PASSWORD: %s", PASSWORD)
logger.debug("SMTP: %s", SMTP)
logger.debug("DB: %s", db)

logger.info("Starting server")


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=False, nullable=False)
    message = db.Column(db.String(200), unique=False, nullable=False)

    def __repr__(self):
        return "<Email(id='%s', email='%s', message='%s')>" % (
            self.id,
            self.email,
            self.message,
        )


db.create_all()
logger.info("Database created")


@app.route("/api", methods=["GET", "POST"])
def index():
    logger.debug(request)
    logger.info("Hello World!")
    return "Hello World!", 200


@app.route("/api/v2/mail", methods=["POST"])
def send_mail_v2():
    if request.method == "POST":
        logger.debug(request)
        email = request.args.get("email", default=None, type=str)
        message = request.args.get("message", default=None, type=str)
        global USERNAME
        global PASSWORD
        global PORT
        global SMTP
        global CONTEXT

        try:
            with smtplib.SMTP_SSL(SMTP, PORT, context=CONTEXT) as server:
                logger.debug("Connecting to %s:%s", SMTP, PORT)
                logger.debug("Logging in with %s:%s", USERNAME, PASSWORD)
                server.login(USERNAME, PASSWORD)
                logger.debug("Sending email to %s:%s", email, message)
                server.sendmail(USERNAME, email, message)
                logger.info("Email sent to %s", email)
                logger.debug(message)
        except Exception as e:
            response = jsonify({"exception": e})
            logger.error(response)
            return response, 500

        db.session.add(Email(email=email, message=message))
        db.session.commit()

        response = jsonify({"message": message, "email": email})
        logging.info(response)
        return response, 200


@app.route("/api/v1/mail/<email>/<message>", methods=["POST"])
def send_mail(email, message):
    if request.method == "POST":
        logger.debug(request)
        global USERNAME
        global PASSWORD
        global PORT
        global SMTP
        global CONTEXT

        try:
            with smtplib.SMTP_SSL(SMTP, PORT, context=CONTEXT) as server:
                logger.debug("Connecting to %s:%s", SMTP, PORT)
                logger.debug("Logging in with %s:%s", USERNAME, PASSWORD)
                server.login(USERNAME, PASSWORD)
                logger.debug("Sending email to %s:%s", email, message)
                server.sendmail(USERNAME, email, message)
                logger.info("Email sent to %s", email)
                logger.debug(message)
        except Exception as e:
            response = jsonify({"exception": e})
            logger.error(response)
            return response, 500

        db.session.add(Email(email=email, message=message))
        db.session.commit()

        response = jsonify({"message": message, "email": email})
        logger.info(response)
        return response, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
