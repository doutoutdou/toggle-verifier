from python:3.7.12-slim-buster
WORKDIR /app
copy requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
copy ./sample .
EXPOSE 5000
CMD [ "python3", "app.py", "--host=0.0.0.0"]
