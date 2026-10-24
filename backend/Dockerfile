FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY contracts /app/contracts
COPY data /app/data
COPY backend /app/backend
COPY eval /app/eval
COPY scripts /app/scripts

ENV PYTHONPATH=/app
ENV DB_PATH=/app/data/payproof.db

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
