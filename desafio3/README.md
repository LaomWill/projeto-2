# Desafio 3 — Docker Compose Orquestrando Serviços

## Objetivo

Usar Docker Compose para orquestrar três serviços interdependentes:
- **Web**: Flask rodando na porta 5000
- **Database**: PostgreSQL para armazenar visitantes
- **Cache**: Redis para estatísticas

## Componentes

| Componente | Descrição |
|-----------|-----------|
| **web** | Aplicação Flask (Python 3.11) porta 5000 |
| **db** | PostgreSQL 15 Alpine - armazena dados |
| **cache** | Redis 7 Alpine - cache de estatísticas |

## Quick Start

### 1. Iniciar todos os serviços
```bash
cd desafio3
docker-compose up -d
```

### 2. Acessar aplicação
```bash
http://localhost:5000
```

### 3. Visualizar logs
```bash
docker-compose logs -f          # Todos
docker-compose logs -f web      # Apenas web
docker-compose logs -f db       # Apenas database
```

### 4. Verificar status
```bash
docker-compose ps
```

## Testes

### Conectar ao PostgreSQL
```bash
docker-compose exec db psql -U appuser -d appdb
```

### Conectar ao Redis
```bash
docker-compose exec cache redis-cli
```

### Testar saúde dos serviços
```bash
curl http://localhost:5000/health
```

## Parar

```bash
docker-compose down           # Mantém volumes
docker-compose down -v        # Remove volumes também
```

## Conceitos-chave

✅ Docker Compose para orquestração  
✅ Dependências entre serviços  
✅ Comunicação por nome (DNS interno)  
✅ Volumes para persistência  
✅ Healthchecks  
✅ Variáveis de ambiente
