FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN dos2unix ./entrypoint.sh
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["sh", "./entrypoint.sh"]
