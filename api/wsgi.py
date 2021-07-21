import csv, smtplib, ssl, configparser, logging, logging.config

import yaml

from flask import Flask, request, jsonify

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("conf.ini")

with open("log.yaml", "r") as conf:
    logger_config = yaml.safe_load(conf.read())
    logging.config.dictConfig(logger_config)

logger = logging.getLogger("main")

USERNAME = config.get("settings", "user")
PASSWORD = config.get("settings", "pass")
PORT = config.getint("settings", "port")
SMTP = config.get("settings", "smtp_server")

logger.info("PORT: %s", PORT)
logger.info("USERNAME: %s", USERNAME)
logger.info("PASSWORD %s", PASSWORD)
logger.info("SMTP: %s", SMTP)


@app.route("api/v1/mail/<email>/<subject>/<message>", methods=["GET", "POST"])
def send_mail(email, subject, message):
    if request.method == "POST":
        global USERNAME
        global PASSWORD
        global PORT
        global SMTP
        content = """\n
            Hello, World!

            This is a test message sent from Python.\n

            {email}\n
            {subject}\n
            {message}\n
            """.format(
            message=message, subject=subject, email=email
        )

        logger.info("Sending mail to %s", email)
        logger.info("Message: %s", content)

        with smtplib.SMTP_SSL(SMTP, PORT, ssl.create_default_context()) as server:
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, email, content)

        response = (
            "Email sent to {email}, subject: {subject}, message: {message}".format(
                message=message, subject=subject, email=email
            )
        )
        logger.info(jsonify(response))
        return response, 200

    if request.method == "GET":
        response = "POST received {0}, subject {1}, message {2}".format(
            email, subject, message
        )
        return f"Mail: {response}", 200
