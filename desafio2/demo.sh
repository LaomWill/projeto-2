#!/bin/bash

echo "=========================================="
echo "Desafio 2 - Volumes e Persistência"
echo "Demonstração Automática"
echo "=========================================="
echo ""

# Criar volume
echo "1. Criando volume Docker 'task-data'..."
docker volume create task-data
echo ""

# Build das imagens
echo "2. Construindo imagens..."
docker build -t task-manager -f Dockerfile.manager .
docker build -t data-reader -f Dockerfile.reader .
echo ""

# Adicionar dados de exemplo
echo "3. Criando dados de exemplo no volume..."
docker run --rm -v task-data:/data task-manager python -c "
import sqlite3
from datetime import datetime

conn = sqlite3.connect('/data/tasks.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'pendente',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
    )
''')

# Adicionar tarefas de exemplo
tasks = [
    ('Estudar Docker', 'Aprender sobre containers e volumes', 'concluída'),
    ('Implementar microsserviços', 'Criar arquitetura de microsserviços', 'pendente'),
    ('Configurar CI/CD', 'Automatizar deploy com GitHub Actions', 'pendente'),
    ('Documentar projeto', 'Escrever README completo', 'concluída'),
]

for title, desc, status in tasks:
    cursor.execute(
        'INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)',
        (title, desc, status)
    )

conn.commit()
conn.close()
print('✓ Dados de exemplo criados!')
"
echo ""

# Ler dados com o primeiro container
echo "4. Lendo dados com o container data-reader..."
docker run --rm -v task-data:/data data-reader
echo ""

# Remover container (dados persistem)
echo "5. Demonstrando persistência: removendo containers..."
docker ps -a | grep task-manager | awk '{print $1}' | xargs -r docker rm -f 2>/dev/null
echo "   Containers removidos, mas dados permanecem no volume!"
echo ""

# Ler dados novamente
echo "6. Lendo dados novamente após remoção dos containers..."
docker run --rm -v task-data:/data data-reader
echo ""

echo "=========================================="
echo "Demonstração concluída!"
echo "=========================================="
echo ""
echo "Os dados persistiram mesmo após a remoção dos containers!"
echo ""
echo "Para usar interativamente:"
echo "  docker run -it --rm -v task-data:/data task-manager"
echo ""
echo "Para inspecionar o volume:"
echo "  docker volume inspect task-data"
echo ""
echo "Para limpar:"
echo "  ./cleanup.sh"
echo ""
