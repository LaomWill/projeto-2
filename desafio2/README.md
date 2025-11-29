# Desafio 2 — Volumes e Persistência

## Objetivo

Demonstrar persistência de dados em Docker usando volumes:
- **Task Manager**: Aplicação interativa que salva tarefas em SQLite
- **Data Reader**: Container que lê dados persistidos
- **Volume task-data**: Armazena `tasks.db` e persiste dados

## Componentes

| Componente | Descrição |
|-----------|-----------|
| **task-manager** | Gerenciador de tarefas com SQLite (Python 3.11) |
| **data-reader** | Leitor de dados do volume |
| **task-data** | Volume Docker para persistência |

## Quick Start

### 1. Executar demonstração
```bash
cd desafio2
./demo.sh
```

### 2. Usar manualmente
```bash
# Criar volume
docker volume create task-data

# Construir imagens
docker build -t task-manager -f Dockerfile.manager .
docker build -t data-reader -f Dockerfile.reader .

# Executar gerenciador (interativo)
docker run -it --rm -v task-data:/data task-manager

# Ler dados em outro terminal
docker run --rm -v task-data:/data data-reader
```

## Comandos Úteis

```bash
# Inspecionar volume
docker volume inspect task-data

# Listar volumes
docker volume ls

# Limpeza
./cleanup.sh
# ou
docker volume rm task-data
docker rmi task-manager data-reader
```

## Conceitos-chave

✅ Volumes Docker para persistência  
✅ Compartilhamento de dados entre containers  
✅ SQLite para armazenamento  
✅ Dados independentes do ciclo de vida dos containers
