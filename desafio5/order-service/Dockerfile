FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask requests

COPY app.py .

EXPOSE 5002

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import requests; requests.get('http://localhost:5002/health')"

CMD ["python", "app.py"]
