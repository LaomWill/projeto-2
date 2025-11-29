from flask import Flask, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

USERS_DATABASE = [
    {
        "id": 1,
        "name": "Ana Silva",
        "email": "ana.silva@email.com",
        "role": "Desenvolvedora",
        "department": "Tecnologia",
        "active": True,
        "joined_date": "2023-01-15"
    },
    {
        "id": 2,
        "name": "Carlos Santos",
        "email": "carlos.santos@email.com",
        "role": "Designer",
        "department": "Criação",
        "active": True,
        "joined_date": "2023-03-20"
    },
    {
        "id": 3,
        "name": "Beatriz Costa",
        "email": "beatriz.costa@email.com",
        "role": "Gerente de Projetos",
        "department": "Gestão",
        "active": True,
        "joined_date": "2022-11-10"
    },
    {
        "id": 4,
        "name": "Daniel Oliveira",
        "email": "daniel.oliveira@email.com",
        "role": "Analista de Dados",
        "department": "Tecnologia",
        "active": False,
        "joined_date": "2023-05-08"
    },
    {
        "id": 5,
        "name": "Elena Rodrigues",
        "email": "elena.rodrigues@email.com",
        "role": "DevOps Engineer",
        "department": "Infraestrutura",
        "active": True,
        "joined_date": "2023-07-22"
    }
]

@app.route('/')
def home():
    """Endpoint raiz com informações do serviço"""
    return jsonify({
        "service": "User Service",
        "version": "1.0.0",
        "description": "Microsserviço de gerenciamento de usuários",
        "endpoints": {
            "GET /users": "Lista todos os usuários",
            "GET /users/<id>": "Retorna usuário específico",
            "GET /users/active": "Lista apenas usuários ativos",
            "GET /health": "Health check do serviço"
        },
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/users', methods=['GET'])
def get_users():
    """Retorna lista completa de usuários"""
    response = {
        "service": "User Service",
        "total": len(USERS_DATABASE),
        "users": USERS_DATABASE,
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"[LOG] GET /users - Retornando {len(USERS_DATABASE)} usuários")
    return jsonify(response), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retorna usuário específico por ID"""
    user = next((u for u in USERS_DATABASE if u['id'] == user_id), None)
    
    if user:
        print(f"[LOG] GET /users/{user_id} - Usuário encontrado: {user['name']}")
        return jsonify({
            "service": "User Service",
            "user": user,
            "timestamp": datetime.now().isoformat()
        }), 200
    else:
        print(f"[LOG] GET /users/{user_id} - Usuário não encontrado")
        return jsonify({
            "service": "User Service",
            "error": "Usuário não encontrado",
            "user_id": user_id
        }), 404

@app.route('/users/active', methods=['GET'])
def get_active_users():
    """Retorna apenas usuários ativos"""
    active_users = [u for u in USERS_DATABASE if u['active']]
    
    response = {
        "service": "User Service",
        "total": len(active_users),
        "users": active_users,
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"[LOG] GET /users/active - Retornando {len(active_users)} usuários ativos")
    return jsonify(response), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check do serviço"""
    return jsonify({
        "service": "User Service",
        "status": "healthy",
        "uptime": "operational",
        "database_records": len(USERS_DATABASE),
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print("="*60)
    print("Microsserviço A - User Service")
    print("Porta: 5001")
    print("="*60)
    app.run(host='0.0.0.0', port=5001, debug=False)
