from python:3.7.12-slim-buster
WORKDIR /app
copy requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
copy ./sample .
EXPOSE 5000
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
