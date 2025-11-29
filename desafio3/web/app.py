from flask import Flask, render_template_string, jsonify, request
import psycopg2
import redis
import os
from datetime import datetime

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'appdb')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASS = os.getenv('DB_PASSWORD', 'apppass')

REDIS_HOST = os.getenv('REDIS_HOST', 'cache')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Visitantes</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: 500;
        }
        input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .visitors-list {
            margin-top: 30px;
        }
        .visitor-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .visitor-name {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        .visitor-time {
            color: #666;
            font-size: 0.9em;
        }
        .services-status {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .service-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin-bottom: 5px;
        }
        .status-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
        }
        .status-online {
            background: #10b981;
            color: white;
        }
        .status-offline {
            background: #ef4444;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Sistema de Visitantes</h1>
        <p class="subtitle">Desafio 3 - Docker Compose com Múltiplos Serviços</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="totalVisits">{{ total_visits }}</div>
                <div class="stat-label">Total de Visitas</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="cacheHits">{{ cache_hits }}</div>
                <div class="stat-label">Cache Hits</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="totalVisitors">{{ total_visitors }}</div>
                <div class="stat-label">Visitantes Registrados</div>
            </div>
        </div>
        
        <form id="visitorForm">
            <div class="form-group">
                <label for="name">Nome do Visitante</label>
                <input type="text" id="name" name="name" required placeholder="Digite seu nome">
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required placeholder="seu@email.com">
            </div>
            <button type="submit">Registrar Visita</button>
        </form>
        
        <div class="visitors-list">
            <h2>Últimos Visitantes</h2>
            <div id="visitorsList">
                {% for visitor in visitors %}
                <div class="visitor-item">
                    <div class="visitor-name">{{ visitor[1] }} ({{ visitor[2] }})</div>
                    <div class="visitor-time">{{ visitor[3] }}</div>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="services-status">
            <h3>Status dos Serviços</h3>
            <div class="service-item">
                <span>🌐 Web Application</span>
                <span class="status-badge status-online">ONLINE</span>
            </div>
            <div class="service-item">
                <span>🗄️ PostgreSQL Database</span>
                <span class="status-badge status-{{ 'online' if db_status else 'offline' }}">{{ 'ONLINE' if db_status else 'OFFLINE' }}</span>
            </div>
            <div class="service-item">
                <span>⚡ Redis Cache</span>
                <span class="status-badge status-{{ 'online' if cache_status else 'offline' }}">{{ 'ONLINE' if cache_status else 'OFFLINE' }}</span>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('visitorForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            
            const response = await fetch('/api/visitor', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            if (response.ok) {
                location.reload();
            }
        });
    </script>
</body>
</html>
'''

def get_db_connection():
    """Conecta ao PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None

def get_redis_connection():
    """Conecta ao Redis"""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
        return r
    except Exception as e:
        print(f"Erro ao conectar ao Redis: {e}")
        return None

def init_database():
    """Inicializa o banco de dados"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visitors (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ Banco de dados inicializado")

@app.route('/')
def index():
    # Incrementar contador de visitas no Redis
    r = get_redis_connection()
    cache_status = False
    total_visits = 0
    cache_hits = 0
    
    if r:
        cache_status = True
        total_visits = r.incr('total_visits')
        cache_hits = int(r.get('cache_hits') or 0)
    
    # Buscar visitantes do banco
    conn = get_db_connection()
    db_status = False
    visitors = []
    total_visitors = 0
    
    if conn:
        db_status = True
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM visitors ORDER BY visited_at DESC LIMIT 10')
        visitors = cursor.fetchall()
        cursor.execute('SELECT COUNT(*) FROM visitors')
        total_visitors = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    
    return render_template_string(
        HTML_TEMPLATE,
        visitors=visitors,
        total_visits=total_visits,
        cache_hits=cache_hits,
        total_visitors=total_visitors,
        db_status=db_status,
        cache_status=cache_status
    )

@app.route('/api/visitor', methods=['POST'])
def add_visitor():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO visitors (name, email) VALUES (%s, %s)',
            (name, email)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        # Incrementar cache hits
        r = get_redis_connection()
        if r:
            r.incr('cache_hits')
        
        return jsonify({'success': True}), 201
    
    return jsonify({'success': False}), 500

@app.route('/health')
def health():
    db_conn = get_db_connection()
    redis_conn = get_redis_connection()
    
    status = {
        'web': 'healthy',
        'database': 'healthy' if db_conn else 'unhealthy',
        'cache': 'healthy' if redis_conn else 'unhealthy'
    }
    
    if db_conn:
        db_conn.close()
    
    return jsonify(status)

if __name__ == '__main__':
    print("Inicializando aplicação web...")
    init_database()
    app.run(host='0.0.0.0', port=5000, debug=False)
