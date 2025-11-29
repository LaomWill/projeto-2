from flask import Flask, jsonify
from datetime import datetime
import socket

app = Flask(__name__)

# Contador de requisições
request_count = 0

@app.route('/')
def home():
    global request_count
    request_count += 1
    
    response_data = {
        "message": "Servidor Web Operacional",
        "hostname": socket.gethostname(),
        "timestamp": datetime.now().isoformat(),
        "request_number": request_count,
        "status": "online"
    }
    
    print(f"[LOG] Requisição #{request_count} recebida de {socket.gethostname()}")
    return jsonify(response_data), 200

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "web-server"}), 200

if __name__ == '__main__':
    print("Servidor iniciando na porta 8080...")
    app.run(host='0.0.0.0', port=8080, debug=False)
