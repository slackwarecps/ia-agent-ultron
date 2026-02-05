FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema se necessário
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Usamos Gunicorn para produção em vez do server de dev do Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5005", "main:app"]