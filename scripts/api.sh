cd ../api
guvicorn --bind 0.0.0.0:5000 app:app
cd ../scripts