FROM python:latest

WORKDIR /

COPY *.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

VOLUME [ "/plugins", "/config", "/data" ]

CMD [ "main.py" ]

ENTRYPOINT ["python3"]