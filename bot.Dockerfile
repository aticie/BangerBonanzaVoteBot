FROM python:3.9-slim

WORKDIR /bonanza

COPY bonanza/requirements.txt .
RUN pip install -r requirements.txt

COPY bonanza /bonanza

ENTRYPOINT ["python", "main.py"]