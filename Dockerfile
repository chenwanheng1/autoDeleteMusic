FROM python:3.7

WORKDIR ./autoDeleteMusic

ADD . .

RUN pip install -r requirements.txt

CMD ["python", "./src/main.py"]