FROM python:3.11-slim

WORKDIR /app

# Install build dependencies & curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and data
COPY . .

# Expose ports: 8000 (Web Dashboard), 5683/udp (CoAP Gateway)
EXPOSE 8000 5683/udp

CMD ["python", "-m", "src.backend.main"]
