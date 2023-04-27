FROM python:3.9-alpine

WORKDIR /usr/src/app

ADD test_content.py .

RUN pip install requests

CMD ["python", "./test_content.py" ]