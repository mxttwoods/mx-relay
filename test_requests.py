import requests


def test_post_email() -> None:
    email = "mattwoods9170@gmail.com"
    message = "hello"
    url: str = f"http://localhost:5000/api/v2/mail?email={email}&message={message}"

    response = requests.post(url)

    print(response.text)

    assert response.request.url == url
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json()["email"] == email
    assert response.json()["message"] == message


# test_post_email() # if not using pytest to run tests - comment out
