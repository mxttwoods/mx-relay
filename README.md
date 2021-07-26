# Python MX Relay

> a python email relay using gmail smtp

## Setup

### Configuration

example `conf.ini`

```ini
[settings]
user = example@gmail.com
pass = imadummypassword
port = 465
smtp_server = smtp.gmail.com
```

### Environment

This `README.md` assumes you are using a UNIX based system with python3

```bash
make venv
# python3 -m venv venv

source venv/bin/activate

make install
# pip3 install -r req.txt
```

## Usage

Run locally

```bash
make run
# gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Run tests

```bash
make test
# python3 -m pytest -sv --html report.html
```

### Docker Usage

Build the image

```bash
make docker-build
# docker build --label mxrelay --tag python-mx-relay:latest .
```

Run the image

```bash
make docker-run
# docker run -d --name mxrelay -p 5000:5000 -p 491:491 python-mx-relay
```

Clean up

```bash
make docker-clean
# docker stop mxrelay
# docker rm -f mxrelay
# docker rmi -f python-mx-relay:latest
```

## REST API

The REST API to the mx-relay is described below.

## POST an Email (v2)

### Request

`POST /api/v2/mail`

```bash
curl --location --request POST 'http://localhost:5000/api/v2/mail?email=mattwoods9170@gmail.com&message=hello'
```

### Response

```console
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 12
Server: Werkzeug/2.0.1 Python/3.9.6
Date: Mon, 26 Jul 2021 00:57:54 GMT

[{"message": "hello", "email": "mattwoods9170@gmail.com"}]
```

## POST an Email (v1)

### Request

`POST /api/v1/mail/<email>/<message>/`

```bash
curl --location --request POST 'http://localhost:5000/api/v1/mail/mattwoods9170@gmail.com/hello'
```

### Response

```console
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 12
Server: Werkzeug/2.0.1 Python/3.9.6
Date: Mon, 26 Jul 2021 00:57:54 GMT

[{"message": "hello", "email": "mattwoods9170@gmail.com"}]
```

## Hello World

### Request

`GET /api/`

```bash
curl -i 'http://localhost:5000/api'
```

### Response

```console
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 12
Server: Werkzeug/2.0.1 Python/3.9.6
Date: Mon, 26 Jul 2021 00:57:54 GMT

[Hello World!%]
```

## Examples

### Bash

```bash
curl --location --request POST 'http://localhost:5000/api/v2/mail?email=mattwoods9170@gmail.com&message=hello'
```

```bash
wget --no-check-certificate --quiet \
  --method POST \
  --timeout=0 \
  --header '' \
   'http://localhost:5000/api/v2/mail?email=mattwoods9170@gmail.com&message=hello'
```

### Python

```python
import requests

url = "http://localhost:5000/api/v2/mail?email=mattwoods9170@gmail.com&message=hello"

payload = {}
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

### Javascript

```javascript
var requestOptions = {
  method: 'POST',
  redirect: 'follow'
}

fetch('http://localhost:5000/api/v2/mail?email=mattwoods9170@gmail.com&message=hello', requestOptions)
  .then((response) => response.text())
  .then((result) => console.log(result))
  .catch((error) => console.log('error', error))
```

```javascript
var http = require('follow-redirects').http
var fs = require('fs')

var options = {
  method: 'POST',
  hostname: 'localhost',
  port: 5000,
  path: '/api/v2/mail?email=mattwoods9170@gmail.com&message=hello',
  headers: {},
  maxRedirects: 20
}

var req = http.request(options, function (res) {
  var chunks = []

  res.on('data', function (chunk) {
    chunks.push(chunk)
  })

  res.on('end', function (chunk) {
    var body = Buffer.concat(chunks)
    console.log(body.toString())
  })

  res.on('error', function (error) {
    console.error(error)
  })
})

req.end()
```

### PHP

```php
<?php

$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'http://localhost:5000/api/v2/mail?email=mattwoods9170@gmail.com&message=hello',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'POST',
));

$response = curl_exec($curl);

curl_close($curl);
echo $response;
```

### GO

```golang
package main

import (
  "fmt"
  "net/http"
  "io/ioutil"
)

func main() {

  url := "http://localhost:5000/api/v2/mail?email=mattwoods9170@gmail.com&message=hello"
  method := "POST"

  client := &http.Client {
  }
  req, err := http.NewRequest(method, url, nil)

  if err != nil {
fmt.Println(err)
return
  }
  res, err := client.Do(req)
  if err != nil {
fmt.Println(err)
return
  }
  defer res.Body.Close()

  body, err := ioutil.ReadAll(res.Body)
  if err != nil {
fmt.Println(err)
return
  }
  fmt.Println(string(body))
}
```
