from flask import Flask, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)

USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://service-users:5001')

ACTIVITIES_DATABASE = {
    1: {"last_login": "2024-11-28 14:30:00", "tasks_completed": 45, "projects": 3},
    2: {"last_login": "2024-11-29 09:15:00", "tasks_completed": 32, "projects": 2},
    3: {"last_login": "2024-11-27 16:45:00", "tasks_completed": 78, "projects": 5},
    4: {"last_login": "2024-10-15 11:20:00", "tasks_completed": 12, "projects": 1},
    5: {"last_login": "2024-11-29 08:00:00", "tasks_completed": 56, "projects": 4}
}

@app.route('/')
def home():
    """Endpoint raiz com informações do serviço"""
    return jsonify({
        "service": "Activity Service",
        "version": "1.0.0",
        "description": "Microsserviço de atividades e estatísticas de usuários",
        "dependencies": {
            "user_service": USER_SERVICE_URL
        },
        "endpoints": {
            "GET /activities": "Lista todas as atividades",
            "GET /activities/<user_id>": "Retorna atividades de usuário específico",
            "GET /users-with-activities": "Combina dados de usuários com suas atividades",
            "GET /health": "Health check do serviço"
        },
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/activities', methods=['GET'])
def get_activities():
    """Retorna todas as atividades"""
    response = {
        "service": "Activity Service",
        "total": len(ACTIVITIES_DATABASE),
        "activities": ACTIVITIES_DATABASE,
        "timestamp": datetime.now().isoformat()
    }
    
    print(f"[LOG] GET /activities - Retornando {len(ACTIVITIES_DATABASE)} registros")
    return jsonify(response), 200

@app.route('/activities/<int:user_id>', methods=['GET'])
def get_user_activities(user_id):
    """Retorna atividades de um usuário específico"""
    activities = ACTIVITIES_DATABASE.get(user_id)
    
    if activities:
        print(f"[LOG] GET /activities/{user_id} - Atividades encontradas")
        return jsonify({
            "service": "Activity Service",
            "user_id": user_id,
            "activities": activities,
            "timestamp": datetime.now().isoformat()
        }), 200
    else:
        print(f"[LOG] GET /activities/{user_id} - Nenhuma atividade encontrada")
        return jsonify({
            "service": "Activity Service",
            "error": "Nenhuma atividade encontrada para este usuário",
            "user_id": user_id
        }), 404

@app.route('/users-with-activities', methods=['GET'])
def get_users_with_activities():
    """
    Endpoint que combina dados do serviço de usuários com atividades
    Demonstra comunicação entre microsserviços via HTTP
    """
    try:
        print(f"[LOG] Requisitando dados do User Service: {USER_SERVICE_URL}/users")
        
        response = requests.get(f"{USER_SERVICE_URL}/users", timeout=5)
        
        if response.status_code != 200:
            print(f"[ERROR] User Service retornou status {response.status_code}")
            return jsonify({
                "service": "Activity Service",
                "error": "Falha ao comunicar com User Service",
                "status_code": response.status_code
            }), 500
        
        users_data = response.json()
        users = users_data.get('users', [])
        
        print(f"[LOG] Recebidos {len(users)} usuários do User Service")
        
        combined_data = []
        for user in users:
            user_id = user['id']
            activities = ACTIVITIES_DATABASE.get(user_id, {
                "last_login": "N/A",
                "tasks_completed": 0,
                "projects": 0
            })
            
            try:
                joined_date = datetime.strptime(user['joined_date'], '%Y-%m-%d')
                days_since_joined = (datetime.now() - joined_date).days
            except:
                days_since_joined = 0
            
            combined_data.append({
                "user_id": user_id,
                "name": user['name'],
                "email": user['email'],
                "role": user['role'],
                "department": user['department'],
                "active": user['active'],
                "joined_date": user['joined_date'],
                "days_since_joined": days_since_joined,
                "last_login": activities.get('last_login'),
                "tasks_completed": activities.get('tasks_completed'),
                "projects": activities.get('projects'),
                "status_message": f"{user['name']} está ativo desde {user['joined_date']} ({days_since_joined} dias) - {activities.get('tasks_completed')} tarefas concluídas"
            })
        
        print(f"[LOG] Dados combinados com sucesso para {len(combined_data)} usuários")
        
        return jsonify({
            "service": "Activity Service",
            "description": "Dados combinados de User Service + Activity Service",
            "total_users": len(combined_data),
            "data": combined_data,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Não foi possível conectar ao User Service em {USER_SERVICE_URL}")
        return jsonify({
            "service": "Activity Service",
            "error": "Não foi possível conectar ao User Service",
            "user_service_url": USER_SERVICE_URL,
            "suggestion": "Verifique se o serviço de usuários está rodando"
        }), 503
        
    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout ao conectar ao User Service")
        return jsonify({
            "service": "Activity Service",
            "error": "Timeout ao conectar ao User Service"
        }), 504
        
    except Exception as e:
        print(f"[ERROR] Erro inesperado: {str(e)}")
        return jsonify({
            "service": "Activity Service",
            "error": "Erro interno do servidor",
            "details": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check do serviço"""
    user_service_status = "unknown"
    try:
        response = requests.get(f"{USER_SERVICE_URL}/health", timeout=2)
        user_service_status = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        user_service_status = "unreachable"
    
    return jsonify({
        "service": "Activity Service",
        "status": "healthy",
        "dependencies": {
            "user_service": user_service_status
        },
        "database_records": len(ACTIVITIES_DATABASE),
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print("="*60)
    print("Microsserviço B - Activity Service")
    print(f"Porta: 5002")
    print(f"User Service URL: {USER_SERVICE_URL}")
    print("="*60)
    app.run(host='0.0.0.0', port=5002, debug=False)
