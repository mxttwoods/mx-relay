import requests
import json
from jsonschema import validate
from jsonschema import Draft6Validator

# {
#   "email": {
#     "subject": "value",
#     "message": "value",
#     "to": "value"
#   }
# }

schema = {
    "$schema": "https://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "email": {
            "type": "object",
            "properties": {
                "subject": {"type": "string"},
                "message": {"type": "string"},
                "to": {"type": "string"},
            },
            "required": ["subject", "message", "to"],
        }
    },
}


def test_post_email():
    response = requests.post(
        "https://localhost/api/v1/mail",
        json={"subject": "value", "message": "value", "to": "value"},
    )

    assert response.request.headers["Content-Type"]
    assert response.request.url == "https://localhost/api/v1/mail"
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    validate(instance=response.json(), schema=schema)
