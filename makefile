docker-build:
	docker build  --label mxrelay --tag python-mx-relay:latest .
docker-run:
	docker run -d --name mxrelay -p 5000:5000 -p 491:491 python-mx-relay
docker-clean:
	docker stop mxrelay
	docker rm -f mxrelay
	docker rmi -f python-mx-relay:latest
test:
	python3 -m pytest -sv --html report.html
run:
	gunicorn -w 4 -b 0.0.0.0:5000 app:app
clean:
	rm -rf app.log
	rm -rf mail.db
	rm -rf report.html
	rm -rf .idea
	rm -rf .pyre
	rm -rf venv
	rm -rf assets
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf .vscode
install:
	pip3 install -r req.txt
venv:
	python3 -m venv venv
	# source venv/bin/activate # not working on macos
quick-test:
	curl -i --location --request POST 'http://localhost:5000/api/v2/mail?email=mattwoods9170@gmail.com&message=hello'