FROM python:2.7

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "-w 3", "-b :80", "app"]
