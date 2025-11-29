# Desafio 5 — Microsserviços com API Gateway

## Objetivo

Implementar um API Gateway como ponto único de entrada para microsserviços:
- **Gateway**: Porta 8080 (única exposta externamente)
- **User Service**: Porta 5001 (interna)
- **Order Service**: Porta 5002 (interna)

## Componentes

| Componente | Descrição |
|-----------|-----------|
| **gateway** | Flask - Roteador para microsserviços :8080 |
| **user-service** | Flask - Gerencia usuários :5001 |
| **order-service** | Flask - Gerencia pedidos :5002 |

## Quick Start

### 1. Iniciar
```bash
cd desafio5
docker-compose up -d
```

### 2. Acessar Dashboard
```bash
http://localhost:8080
```

### 3. Testar API

**Listar usuários:**
```bash
curl http://localhost:8080/users
curl http://localhost:8080/users/1
```

**Listar pedidos:**
```bash
curl http://localhost:8080/orders
curl http://localhost:8080/orders/user/1
```

**Health check:**
```bash
curl http://localhost:8080/health
```

### 4. Verificar isolamento

**Microsserviços NÃO acessíveis externamente:**
```bash
curl http://localhost:5001/users  # Falha
curl http://localhost:5002/orders # Falha
```

### 5. Visualizar logs
```bash
docker-compose logs -f           # Todos
docker-compose logs -f gateway   # Gateway
```

### 6. Testar resiliência

**Parar User Service:**
```bash
docker-compose stop user-service

# Gateway retorna erro apropriado
curl http://localhost:8080/users

# Health mostra serviço degradado
curl http://localhost:8080/health

# Reiniciar
docker-compose start user-service
```

### 7. Parar
```bash
docker-compose down
```

## Conceitos-chave

✅ Padrão API Gateway  
✅ Ponto único de entrada  
✅ Roteamento de requisições  
✅ Isolamento de microsserviços  
✅ Health check agregado  
✅ Orquestração com Docker Compose  
✅ Segurança por isolamento
