FROM python:3.9-alpine

WORKDIR /usr/src/app

ADD test_authorization.py .

RUN pip install requests

CMD ["python", "./test_authorization.py" ]