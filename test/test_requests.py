import requests


def test_post_email():
    email = "mattwoods9170@gmail.com"
    message = "hello"
    url = f"http://localhost:5000/api/v2/mail?email={email}&message={message}"

    response = requests.post(url)

    assert response.request.url == url
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json()["email"] == email
    assert response.json()["message"] == message
    assert response.json()["status"] == "success"
