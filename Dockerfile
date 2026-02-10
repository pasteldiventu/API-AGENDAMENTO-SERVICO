FROM python:3.12-slim

WORKDIR /app

# Evita gerar .pyc e melhora logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependências de sistema mínimas (se precisar compilar algo no futuro)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app ./app

# Porta exposta pelo Uvicorn
EXPOSE 8000

# Comando padrão: cria as tabelas e sobe o servidor
CMD ["sh", "-c", "python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000"]


