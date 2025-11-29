from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

USERS = [
    {"id": 1, "name": "João Silva", "email": "joao@email.com", "role": "Admin", "status": "active"},
    {"id": 2, "name": "Maria Santos", "email": "maria@email.com", "role": "User", "status": "active"},
    {"id": 3, "name": "Pedro Costa", "email": "pedro@email.com", "role": "User", "status": "inactive"},
    {"id": 4, "name": "Ana Oliveira", "email": "ana@email.com", "role": "Manager", "status": "active"},
    {"id": 5, "name": "Carlos Lima", "email": "carlos@email.com", "role": "User", "status": "active"}
]

@app.route('/')
def home():
    return jsonify({
        "service": "User Service",
        "version": "2.0.0",
        "description": "Microsserviço de gerenciamento de usuários",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/users', methods=['GET'])
def get_users():
    print(f"[USER-SERVICE] GET /users - Retornando {len(USERS)} usuários")
    return jsonify({
        "service": "User Service",
        "total": len(USERS),
        "users": USERS,
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in USERS if u['id'] == user_id), None)
    if user:
        print(f"[USER-SERVICE] GET /users/{user_id} - Usuário: {user['name']}")
        return jsonify({"service": "User Service", "user": user}), 200
    else:
        print(f"[USER-SERVICE] GET /users/{user_id} - Não encontrado")
        return jsonify({"error": "Usuário não encontrado"}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "service": "User Service",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print("User Service iniciando na porta 5001...")
    app.run(host='0.0.0.0', port=5001, debug=False)
