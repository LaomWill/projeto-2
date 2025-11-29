FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
RUN pip install --no-cache-dir flask psycopg2-binary redis

# Copiar código da aplicação
COPY app.py .

# Expor porta
EXPOSE 5000

# Comando de inicialização
CMD ["python", "app.py"]
