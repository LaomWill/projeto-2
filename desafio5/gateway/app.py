from flask import Flask, jsonify, request, render_template_string
import requests
from datetime import datetime
import os

app = Flask(__name__)

USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5001')
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://order-service:5002')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Gateway - Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        h1 {
            color: #1e3c72;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .services {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .service-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .service-title {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .service-endpoints {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            font-size: 0.9em;
        }
        .endpoint {
            padding: 8px;
            margin: 5px 0;
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .endpoint:hover {
            background: rgba(255,255,255,0.2);
        }
        .endpoint code {
            color: #ffd700;
        }
        .gateway-info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .gateway-info h3 {
            color: #1e3c72;
            margin-bottom: 10px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .info-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .info-label {
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
        }
        .info-value {
            font-size: 1.1em;
            font-weight: bold;
            color: #333;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-online { background: #10b981; }
        .status-offline { background: #ef4444; }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 API Gateway Dashboard</h1>
        <p class="subtitle">Desafio 5 - Microsserviços com API Gateway</p>
        
        <div class="gateway-info">
            <h3>Informações do Gateway</h3>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Status do Gateway</div>
                    <div class="info-value">
                        <span class="status-indicator status-online"></span>
                        ONLINE
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-label">Microsserviços Conectados</div>
                    <div class="info-value">2 Serviços</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Versão</div>
                    <div class="info-value">v1.0.0</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Timestamp</div>
                    <div class="info-value">{{ timestamp }}</div>
                </div>
            </div>
        </div>
        
        <div class="services">
            <div class="service-card">
                <div class="service-title">
                    👥 User Service
                </div>
                <div class="service-endpoints">
                    <div class="endpoint">
                        <code>GET /users</code><br>
                        Lista todos os usuários
                    </div>
                    <div class="endpoint">
                        <code>GET /users/:id</code><br>
                        Busca usuário por ID
                    </div>
                </div>
                <div style="margin-top: 15px; font-size: 0.9em;">
                    <strong>Status:</strong> 
                    <span class="status-indicator status-{{ 'online' if user_service_status else 'offline' }}"></span>
                    {{ 'ONLINE' if user_service_status else 'OFFLINE' }}
                </div>
            </div>
            
            <div class="service-card">
                <div class="service-title">
                    📦 Order Service
                </div>
                <div class="service-endpoints">
                    <div class="endpoint">
                        <code>GET /orders</code><br>
                        Lista todos os pedidos
                    </div>
                    <div class="endpoint">
                        <code>GET /orders/:id</code><br>
                        Busca pedido por ID
                    </div>
                    <div class="endpoint">
                        <code>GET /orders/user/:id</code><br>
                        Pedidos de um usuário
                    </div>
                </div>
                <div style="margin-top: 15px; font-size: 0.9em;">
                    <strong>Status:</strong> 
                    <span class="status-indicator status-{{ 'online' if order_service_status else 'offline' }}"></span>
                    {{ 'ONLINE' if order_service_status else 'OFFLINE' }}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Como usar:</strong> Acesse os endpoints através do gateway na porta 8080</p>
            <p style="margin-top: 10px;">Exemplo: <code>curl http://localhost:8080/users</code></p>
        </div>
    </div>
</body>
</html>
'''

def check_service_health(url):
    """Verifica se um serviço está saudável"""
    try:
        response = requests.get(f"{url}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

@app.route('/')
def home():
    """Dashboard do Gateway"""
    user_service_status = check_service_health(USER_SERVICE_URL)
    order_service_status = check_service_health(ORDER_SERVICE_URL)
    
    return render_template_string(
        HTML_TEMPLATE,
        timestamp=datetime.now().strftime("%H:%M:%S"),
        user_service_status=user_service_status,
        order_service_status=order_service_status
    )

@app.route('/api')
def api_info():
    """Informações da API"""
    return jsonify({
        "service": "API Gateway",
        "version": "1.0.0",
        "description": "Gateway centralizando acesso aos microsserviços",
        "services": {
            "user_service": USER_SERVICE_URL,
            "order_service": ORDER_SERVICE_URL
        },
        "endpoints": {
            "users": [
                "GET /users - Lista todos os usuários",
                "GET /users/<id> - Busca usuário específico"
            ],
            "orders": [
                "GET /orders - Lista todos os pedidos",
                "GET /orders/<id> - Busca pedido específico",
                "GET /orders/user/<user_id> - Pedidos de um usuário"
            ]
        },
        "timestamp": datetime.now().isoformat()
    }), 200

# ==================== ROTAS DE USUÁRIOS ====================

@app.route('/users', methods=['GET'])
def get_users():
    """Proxy para User Service - Lista usuários"""
    try:
        print(f"[GATEWAY] Redirecionando GET /users para {USER_SERVICE_URL}")
        response = requests.get(f"{USER_SERVICE_URL}/users", timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        print(f"[GATEWAY] Erro: User Service indisponível")
        return jsonify({
            "error": "User Service indisponível",
            "service": "API Gateway"
        }), 503
    except Exception as e:
        print(f"[GATEWAY] Erro: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Proxy para User Service - Busca usuário por ID"""
    try:
        print(f"[GATEWAY] Redirecionando GET /users/{user_id} para {USER_SERVICE_URL}")
        response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}", timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "User Service indisponível"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== ROTAS DE PEDIDOS ====================

@app.route('/orders', methods=['GET'])
def get_orders():
    """Proxy para Order Service - Lista pedidos"""
    try:
        print(f"[GATEWAY] Redirecionando GET /orders para {ORDER_SERVICE_URL}")
        response = requests.get(f"{ORDER_SERVICE_URL}/orders", timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        print(f"[GATEWAY] Erro: Order Service indisponível")
        return jsonify({
            "error": "Order Service indisponível",
            "service": "API Gateway"
        }), 503
    except Exception as e:
        print(f"[GATEWAY] Erro: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Proxy para Order Service - Busca pedido por ID"""
    try:
        print(f"[GATEWAY] Redirecionando GET /orders/{order_id} para {ORDER_SERVICE_URL}")
        response = requests.get(f"{ORDER_SERVICE_URL}/orders/{order_id}", timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Order Service indisponível"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    """Proxy para Order Service - Pedidos de um usuário"""
    try:
        print(f"[GATEWAY] Redirecionando GET /orders/user/{user_id} para {ORDER_SERVICE_URL}")
        response = requests.get(f"{ORDER_SERVICE_URL}/orders/user/{user_id}", timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Order Service indisponível"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health():
    """Health check do Gateway e serviços"""
    user_service_status = check_service_health(USER_SERVICE_URL)
    order_service_status = check_service_health(ORDER_SERVICE_URL)
    
    overall_status = "healthy" if (user_service_status and order_service_status) else "degraded"
    
    return jsonify({
        "service": "API Gateway",
        "status": overall_status,
        "services": {
            "user_service": "healthy" if user_service_status else "unhealthy",
            "order_service": "healthy" if order_service_status else "unhealthy"
        },
        "timestamp": datetime.now().isoformat()
    }), 200 if overall_status == "healthy" else 503

if __name__ == '__main__':
    print("="*60)
    print("API Gateway")
    print(f"User Service: {USER_SERVICE_URL}")
    print(f"Order Service: {ORDER_SERVICE_URL}")
    print("Porta: 8080")
    print("="*60)
    app.run(host='0.0.0.0', port=8080, debug=False)
