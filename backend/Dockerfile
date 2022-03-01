FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /bonanza

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY api.py api.py

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8989"]