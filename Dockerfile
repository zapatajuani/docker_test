FROM python:3.10.16-alpine3.21

WORKDIR /app

COPY src/ ./

RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir asyncpg databases

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]