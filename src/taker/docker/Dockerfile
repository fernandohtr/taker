FROM python:3.11-alpine

WORKDIR /opt/app

COPY ./requirements/base.txt .

RUN pip install -r base.txt

COPY .. .

CMD ["python", "run.py"]
