FROM python:3.9-slim

WORKDIR /app

COPY bonanza/requirements.txt .
RUN pip install -r requirements.txt

COPY bonanza /app/bonanza

ENV PYTHONPATH="${PYTHONPATH}:/app/bonanza"

ENTRYPOINT ["python", "bonanza/main.py"]