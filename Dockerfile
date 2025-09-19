FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends tesseract-ocr && rm -rf /var/lib/apt/lists/*
COPY server/requirements.txt /app/server/requirements.txt
RUN pip install --no-cache-dir -r /app/server/requirements.txt
COPY index.html /app/index.html
COPY assets /app/assets
COPY server/app /app/app
COPY server/alembic.ini /app/alembic.ini
COPY server/migrations /app/migrations
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080"]
