FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

WORKDIR /backend

COPY backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY backend/api.py api.py
COPY bonanza bonanza

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8989"]