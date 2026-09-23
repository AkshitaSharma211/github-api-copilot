FROM python:3.12-slim

WORKDIR /app

# build-essential needed for a few packages (e.g. sentence-transformers deps) that
# don't ship prebuilt wheels for every platform
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=120 --retries 5 torch==2.11.0 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir --default-timeout=120 --retries 5 -r requirements.txt

COPY . .

# Render sets $PORT at runtime; shell form so the variable actually expands
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]