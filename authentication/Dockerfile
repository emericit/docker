FROM python:3.9-alpine

WORKDIR /usr/src/app

ADD test_authentication.py .

RUN pip install requests

CMD ["python", "./test_authentication.py" ]