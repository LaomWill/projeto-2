FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask requests

COPY app.py .

EXPOSE 5001

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import requests; requests.get('http://localhost:5001/health')"

CMD ["python", "app.py"]
