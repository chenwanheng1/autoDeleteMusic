FROM python:3.7

WORKDIR ./docker_demo

ADD . .

RUN pip install -r requirements.txt

CMD ["python", "./src/main.py"]