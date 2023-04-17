FROM python:3.11-alpine

WORKDIR /opt/app

COPY ./requirements/base.txt .

RUN pip install -r base.txt

COPY .. .

EXPOSE 8000

CMD ["python", "app.py"]
