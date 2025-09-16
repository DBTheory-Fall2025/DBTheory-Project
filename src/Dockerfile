FROM python:3.9-slim
WORKDIR /app
COPY . .

# Install system dependencies needed for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python", "main.py" ]