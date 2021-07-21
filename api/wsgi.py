import csv, smtplib, ssl, configparser, logging, logging.config

import yaml

from flask import Flask, request, jsonify

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("conf.ini")

USERNAME = config.get("settings", "user")
PASSWORD = config.get("settings", "pass")
PORT = config.getint("settings", "port")
SMTP = config.get("settings", "smtp_server")

with open("log.yaml", "r") as conf:
    logger_config = yaml.safe_load(conf.read())
    logging.config.dictConfig(logger_config)

logger = logging.getLogger("main")

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

        try:
            with smtplib.SMTP_SSL(SMTP, PORT, ssl.create_default_context()) as server:
                server.login(USERNAME, PASSWORD)
                server.sendmail(USERNAME, email, content)
        except Exception as e:
            logger.error(e)
            return jsonify({"status": "error"})

        response = "Email sent to {0}, content: {1}".format(email, content)
        logger.info(jsonify({"response": response}))
        return response, 200

    if request.method == "GET":
        response = "Email sent to {0}, content: {1}".format(email, content)
        logger.info(jsonify({"response": response}))
        return response, 200
